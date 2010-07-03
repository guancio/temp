(require 'bbdb)
(bbdb-initialize)
(require 'bbdb-vcard-import)

(defun wicked/vcard-parse-region (beg end &optional filter)
  "Parse the raw vcard data in region, and return an alist representing data.
This function is just like vcard-parse-string except that it operates on
a region of the current buffer rather than taking a string as an argument.
Note: this function modifies the buffer!"
  (or filter
      (setq filter 'vcard-standard-filter))
  (let ((case-fold-search t)
        (vcard-data nil)
        (pos (make-marker))
        (newpos (make-marker))
        properties value)
    (save-restriction
      (narrow-to-region beg end)
      (save-match-data
        ;; Unfold folded lines and delete naked carriage returns
        (goto-char (point-min))
        (while (re-search-forward "\r$\\|\n[ \t]" nil t)
          (goto-char (match-beginning 0))
          (delete-char 1))
        (goto-char (point-min))
        (re-search-forward "^begin:[ \t]*vcard[ \t]*\n")
        (set-marker pos (point))
        (while (and (not (looking-at "^end[ \t]*:[ \t]*vcard[ \t]*$"))
                    (re-search-forward ":[ \t]*" nil t))
          (set-marker newpos (match-end 0))
          (setq properties
                (vcard-parse-region-properties pos (match-beginning 0)))
          (set-marker pos (marker-position newpos))
          (re-search-forward "\n[-A-Z0-9;=]+:")   ;; change to deal with multiline
          (set-marker newpos (1+ (match-beginning 0))) ;; change to deal with multiline
          (setq value
                (vcard-parse-region-value properties pos (match-beginning 0)))
          (set-marker pos (marker-position newpos))
          (goto-char pos)
          (funcall filter properties value)
          (setq vcard-data (cons (cons properties value) vcard-data)))))
    (nreverse vcard-data)))
;; Replace vcard.el's definition
(fset 'vcard-parse-region 'wicked/vcard-parse-region)

(defun my-convert-name (name)
  (let* ((names (split-string name ", "))
	 (n1 (nth 0 names))
	 (n2 (nth 1 names))
	 )
    (if (not (eq n2 nil))
	(format "%s %s" n2 n1)
      n1
      )))

(defun wicked/bbdb-vcard-merge (record)
  "Merge data from vcard interactively into bbdb."
  (let* ((name (bbdb-vcard-values record "fn"))
	 (company (bbdb-vcard-values record "org"))
	 (net (bbdb-vcard-get-emails record))
	 (addrs (bbdb-vcard-get-addresses record))
	 (phones (bbdb-vcard-get-phones record))
	 (categories (bbdb-vcard-values record "categories"))
	 (notes (and (not (string= "" categories))
		     (list (cons 'categories categories))))
	 ;; TODO: addrs are not yet imported.  To do this right,
	 ;; figure out a way to map the several labels to
	 ;; `bbdb-default-label-list'.  Note, some phone number
	 ;; conversion may break the format of numbers.
	 (bbdb-north-american-phone-numbers-p nil)
	 (n (bbdb-vcard-values record "n"))
	 (normal-name (if (not (eq n "")) n name))
	 (normal-name (if (not (eq normal-name "")) normal-name company))
	 (company (if (not (eq normal-name company)) company ""))
	 (normal-name (if (not (eq normal-name "")) normal-name "Unnamed"))
	 (normal-name (my-convert-name normal-name))
	 (new-record (bbdb-vcard-merge-interactively normal-name
	 ;; (new-record (bbdb-vcard-merge-interactively name
						     company
						     net
						     nil ;; Skip addresses
						     phones ;; Include phones
						     notes)))
    (setq bbdb-vcard-merged-records (append bbdb-vcard-merged-records
					    (list new-record)))))
;; Replace bbdb-vcard-import.el's definition
(fset 'bbdb-vcard-merge 'wicked/bbdb-vcard-merge)

(require 'bbdb-vcard-export)


;; (setq bbdb-file "~/Desktop/sync/tmp.bbdb")
;; (bbdb-initialize)

;; apply a function to all files in a dir
(require 'find-lisp)
(require 'bbdb-merge)

(defun my-bbdb-vcard-import (file)
  "Import the vcards in FILE into your bbdb."
  (interactive "FvCard file to read from: ")
  (let ((buffer (find-file file)))
    (switch-to-buffer buffer)
    (beginning-of-buffer)
    (replace-regexp "tel;cell" "tel;type=Mobile")
    (beginning-of-buffer)
    (replace-regexp "tel;voice" "tel;type=Home")
    (beginning-of-buffer)
    (replace-regexp "tel;home" "tel;type=Home")
    (beginning-of-buffer)
    (replace-regexp "tel;work" "tel;type=Work")
    (beginning-of-buffer)
    (replace-regexp "tel:" "tel;type=Home:")
    (beginning-of-buffer)
    (bbdb-vcard-snarf-buffer buffer)
    (revert-buffer buffer t t)
    (kill-buffer buffer))
  )


;;(defun bbdb-merge-internally 'bbdb-merge-record)
(defun bbdb-merge-internally (old-record new-record)
  (bbdb-merge-record new-record old-record)
)



(defun guancio-bbdb-sync-hook (record)
  (bbdb-record-putprop record 'sync "Yes")
)

(defun guancio-bbdb-sync ()
  (remove-hook 'bbdb-create-hook 'guancio-bbdb-imported-hook)
  (add-hook 'bbdb-create-hook 'guancio-bbdb-sync-hook)
  (mapc 'my-bbdb-vcard-import (find-lisp-find-files "/tmp/guancio" ".$"))
  (add-hook 'bbdb-create-hook 'guancio-bbdb-imported-hook)
  (remove-hook 'bbdb-create-hook 'guancio-bbdb-sync-hook)
)

;; (guancio-bbdb-sync)
;; (bbdb-vcard-export-update-all "/tmp/guancio3/" 'latin-1)


