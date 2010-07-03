(def stream '(
    ("element", "person", ""),
    ("attr", "name", "a"),
    ("attr", "surname", "b"),
    ("element", "child", ""),
    ("attr", "age", "10"),
    ("end_element", "child", ""),
    ("element", "child", ""),
    ("attr", "age", "20"),
    ("end_element", "child", ""),
    ("element", "child", ""),
    ("end_element", "child", ""),
    ("end_element", "person", ""),
    ("element", "person", ""),
    ("attr", "name", "c"),
    ("attr", "surname", "d"),
    ("end_element", "person", "")
    ))

(defn zero [inp] '())
(defn result [v] 
  (fn [inp] (list (list v inp)))
  )
(defn item [inp]
  (if (= '() inp)
    '()
    (list (list (first inp) (rest inp)))
    ))
(defn bind [p]
  (fn [f]
    (fn [inp]
       (map (fn [[v inp1]]
       	      ((f v) inp1))
       	    (p inp))
      )))
(def attribute
     ((bind item)
      (fn [[event name value]]
	(if (= "attr" event)
	  (result {name value})
	  zero))))
(defn plus [p]
     (fn  [q]
       (fn [inp]
	 (concat (p inp) (q inp)))))
(def attr-list
     ((plus
       (result {}))
      ((bind attribute) (fn [att]
      ((bind attr-list) (fn [ats]
			(result (merge att ats))
			))))))

