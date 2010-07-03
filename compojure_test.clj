(use 'compojure)

(def users 
     [
      {:login       "guancio"
       :password    "roberto"
       :description "Roberto guanciale"
       }
      {:login       "aaa"
       :password    "aaa1"
       :description "aaa2"
       }
      {:login       "bbb"
       :password    "bbb1"
       :description "bbb2"
       }
      {:login       "ccc"
       :password    "ccc1"
       :description "ccc2"
       }
      ]
     )

(defn find-user [login]
  (first (filter (fn [u] (= login (u :login)))
	  users))
  )

(defroutes greeter
  (GET "/"
    (html [:h1 "Hello World"]))
  (GET "/guancio"
    (html [:h1 "Cia guancio"]))
  (GET "/list"
    (html [:h1 "List of all users"]
	  [:table {:border 1}
	   [:tr
	    [:th "Login"]
	    [:th "Description"]
	    [:th ""]
	    
	   (map (fn [u]
		  [:tr 
		   [:td (u :login)]
		   [:td (u :description)]
		   [:td [:a {:href (str "/detail?login=" (u :login))} "[Details]"]]
		   ]
		  )
		users)
	    ]
	   ]

	  )
    )


  (GET "/detail" 
    (html [:div "Elenco delle proprieta'"]
	  [:table {:border 1}
	   [:tr
	    [:th "Key"]
	    [:th "Value"]
	    [:th ""]
	    ]
	   (map (fn [[key value]]
		  [:tr
		   [:td key]
		   [:td value]
		   [:td [:button "Delete"]]
		   ]
		  )
		(find-user ((request :params) :login))
		)
	   ]
	  [:div request]
	  ))
  (ANY "*" 
    (html [:h1 ({:title "ciao"} :title)]
	  [:a {:href "http://www,google.com"} "ciao io sono roberto"]
	  [:img {:src "http://www.bestinclass.dk/wp-content/uploads/avatars/html.png"}]
	  ))
  )

(defserver my-server
  {:port 8082}
  "/*" (servlet greeter))

;; (start my-server)
;;(stop my-server)
