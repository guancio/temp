;; This buffer is for notes you don't want to save, and for Lisp evaluation.
;; If you want to create a file, visit that file with C-x C-f,
;; then enter the text in that file's own buffer.

(defun guancio-complete (&optional start-pos)
  (interactive)
  (let* ((end (point))
         (beg (or start-pos
                  (save-excursion
                    (re-search-backward "\\(\\`\\|[\n:,]\\)[ \t]*")
                    (goto-char (match-end 0))
                    (point))))
         (orig (buffer-substring beg end))
         (typed (downcase orig))
         (pattern (bbdb-string-trim typed))
         (ht (bbdb-hashtable))
         ;; make a list of possible completion strings
         ;; (all-the-completions), and a flag to indicate if there's a
         ;; single matching record or not (only-one-p)
         (only-one-p t)
         (all-the-completions nil)
         (pred
          (lambda (sym)
            (when (bbdb-completion-predicate sym)
              (if (and only-one-p
                       all-the-completions
                       (or
                        ;; not sure about this. more than one record
                        ;; attached to the symbol? does that happen?
                        (> (length (symbol-value sym)) 1)
                        ;; this is the doozy, though. multiple syms
                        ;; which all match the same record
                        (delete t (mapcar (lambda(x)
                                            (equal (symbol-value x)
                                                   (symbol-value sym)))
                                          all-the-completions))))
                  (setq only-one-p nil))
              (if (not (memq sym all-the-completions))
                  (setq all-the-completions (cons sym all-the-completions))))))
         (completion (progn (all-completions pattern ht pred) (try-completion pattern ht)))
         (exact-match (eq completion t)))
    (message completion)
    )
  )

(message 
 (car
  (bbdb-record-phones
   (car
    (symbol-value
     (intern-soft "guancio@gmail.com" (bbdb-hashtable))
     )
    )
   )
  )
 )


(message
 (bbdb-record-phones
  (car
   (bbdb-search (bbdb-records) "giulia" nil nil nil nil)
   )
  )
)



