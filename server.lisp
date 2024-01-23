;; The Language of the Server doens't matter since it's only running on one computer

(require :aserve)

(defpackage :server
  (:use :common-lisp :cl-user :net.aserve :sb-thread :net.html.generator :sb-ext))

(in-package :server)

(start :port 8000)

(defun secure-password ()
  (sxhash (random 1234567890)))

(defvar games  (make-hash-table))
(defglobal *game-number* 0)
(proclaim `(type fixnum *game-number*))

(defvar *game-queue-mutex* (make-mutex :name "game queue mutex"))

(defvar *last-cons* NIL)
(defvar *game-queue* NIL)

(defun add-game-to-queue (game)
  (with-mutex (*game-queue-mutex*)
    (if (not *game-queue*)
	(progn
	  (setf *game-queue* `(,game))
	  (setf *last-cons* *game-queue*))
	(progn
	  (setf (cdr *last-cons*) `(,game))
	  (setf *last-cons* (cdr *last-cons*))))))

(defun pop-game-queue ()
  (with-mutex (*game-queue-mutex*)
    (and *game-queue* (pop *game-queue*))))
  
      
(defun generate-key ()
  (let ((game-number (atomic-incf *game-number*))
	(key (secure-password)))
    (setf (gethash game-number games) `(:x-key ,key))
    (add-game-to-queue game-number)
    (values game-number key)))

(defun find-game ()
  (let ((game (pop-game-queue)))
    (if game
	(let ((key (secure-password)))
	  (setf (gethash game games) `(NIL :o-key ,key . ,(gethash game games)))
	  (values game key)))))


(publish :path "/newgame"
	 :content-type "text/plain"
	 :function
	 #'(lambda (req ent)
             (with-http-response (req ent)
               (with-http-body (req ent)
                 (multiple-value-bind (game-number passcode) (find-game)
		   (multiple-value-bind (game-number passcode) (if (not game-number) (generate-key) (values game-number passcode))
		     (format *html-stream* "Game Number:~A Passcode:~A"  game-number passcode)))))))



(defmacro with-valid-game (&rest body)
  `(let ((game (request-query-value "game" req))
	 (key  (request-query-value "key" req)))
     (let ((game-data (and game (gethash (parse-integer game
							:junk-allowed T)
					 games NIL))))
       
       (if (not game-data)
	   (format *html-stream* "ERROR: Game Not Found")
	   (let* ((key (and key (parse-integer key :junk-allowed T)))
		  (key (first (member key game-data))))
	     (if (not key)
		 (format *html-stream* "ERROR: Key Not Found")
		 (progn
		   . ,body)))))))

  

(defun get-x-or-o (key game-data)
  (cond ((eq (second (member :o-key game-data)) key) :o)
	((eq (second (member :x-key  game-data)) key) :x)))
  

(publish :path "/am-i-x-or-o"
	 :content-type "text/plain"
	 :function
	 #'(lambda (req ent)
             (with-http-response (req ent)
               (with-http-body (req ent)
		 (with-valid-game
		     (case (get-x-or-o key game-data)
		       ((:o)  (format *html-stream* "You are O."))
		       ((:x) (format *html-stream* "You are X."))
		       (T (format *html-stream* "Error: You are Neither."))))))))
(publish :path "/move"
	 :content-type "text/plain"
	 :function
	 #'(lambda (req ent)
             (with-http-response (req ent)
               (with-http-body (req ent)
		 (with-valid-game
		     (block checking-for-valid-move
		       
		       (let* ((move (request-query-value "move" req))
			      (move (and move (or (parse-integer move :junk-allowed T)
						  (and (equalp "q" move) "q")
						  (and (equalp "r" move) "r"))))
			      (x-or-o (case (get-x-or-o key game-data)
					((:x) :x)
					((:o) :o)
				      (T
				       (format *html-stream* "Error: You are Neither X or O.")
				       (return-from checking-for-valid-move)))))
			 (cond ((not move)
				(format *html-stream* "ERROR: move Not Found"))
			       ((cond ((and (consp (first game-data))
					    (member "q" (first game-data) :test #'(lambda (a b) (and (equalp a (second b))))))
				       T)
				      ((and (not (equalp move "q")) (not (equalp move "r")))
				       (cond ((and (eq x-or-o :o)
						(not (third game-data)))
					      T)
					     ((eq x-or-o (first (first (first game-data))))
					      T))))
				(format *html-stream* "Error: It's not your move"))     			       			       
			       ((member move (first game-data) :test #'(lambda (a b) (and (eq a (second b)))))
				(format *html-stream* "Error: move ~A already moved" move))
			       ((not (or (equalp "q" move) (<= 1 move 9)))
				(format *html-stream* "Error: move ~A out of bounds" move))
			       (T
				(format *standard-output* "~% GAME DATA:~A~%" game-data)
				(atomic-push `(,x-or-o ,move) (car game-data))
				(format *standard-output* "~% GAME DATA:~A~%" game-data)
				(format *html-stream* "ok"))))))))))


(publish :path "/lastmove"
	 :content-type "text/plain"
	 :function
	 #'(lambda (req ent)
             (with-http-response (req ent)
               (with-http-body (req ent)
		 (with-valid-game
		   (if (third game-data)
		       (let ((last-move (first (first game-data))))
			 (if last-move
			     (format *html-stream* "Player:~A Position:~A" (if (eq (first last-move) :o) "O" "X")
				     (second last-move))
			     (format *html-stream* "Error: No last move")))
		       (format *html-stream* "Error: No last move")))))))
		       
			     


