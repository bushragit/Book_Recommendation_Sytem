from flask import Flask,render_template,request
app = Flask(__name__)
import pandas as pd
import numpy as np





import pickle
import numpy as np
popular_books = pickle.load(open('popular.pkl',"rb"))
pt = pickle.load(open("pt.pkl","rb"))
book = pickle.load(open("books.pkl","rb"))
similarity_score = pickle.load(open("similarity_score.pkl","rb"))




@app.route('/')
def index():
    return render_template("index.html",
                           book_name = list(popular_books["Book-Title"].values),
                           author = list(popular_books["Book-Author"].values),
                           image = list(popular_books["Image-URL-M"].values),
                           votes = list(popular_books["num-ratings"].values),
                           rating = list(popular_books["avg-ratings"].values),
                             )


@app.route("/recommend")
def recommend_ui():
    return render_template("recommend.html")

@app.route("/recommend_books", methods=["POST"])
def recommend():
    user_input = request.form.get("user_input")
    
    # Check if user input exists in index
    if user_input not in pt.index:
        error_message = f"Sorry, '{user_input}' is not found in our database."
        return render_template("recommend.html", error_message=error_message)
    
    index = np.where(pt.index == user_input)[0][0]
    
    similar_items = sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1], reverse=True)[1:6]
    data = []
    for i in similar_items:
        items = []
        temp_df = book[book["Book-Title"]==pt.index[i[0]]]
        items.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
        items.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
        items.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))

        data.append(items)

    print(data)
    return render_template("recommend.html", data=data)



    

if __name__ =="__main__":
    app.run(debug=True)


