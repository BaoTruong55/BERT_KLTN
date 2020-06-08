
from flask import Flask, request, Response
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
from infer_predict import *
from post_crawl import *
from model_vnexpress import *


# TODO ==== Main ===============================================================


app = Flask(__name__)
api = Api(app)

class Vnexpress(Resource):
    def get(self):
        url = request.args.get('url')
        idPost, title, description, thumbnailUrl =  getInfoPost(url)
        comments = getComments(idPost)

        if len(comments) == 0:
            return {"Error": "The article has no comments"}
        
        df = NomalizeData(comments)
        df_result = PredictData(df)
        df_output = DataFrame(df_result, columns= ['data_text', 'label'])
        df_negatives = df_output[df_output['label'] == 0]
        df_possitives = df_output[df_output['label'] == 1]
        
        output = {
            "title": title,
            "description": description,
            "thumbnailUrl": thumbnailUrl,
            "pos": len(df_possitives.index),
            "neg": len(df_negatives.index),
            "commentPos": df_possitives.to_dict("records"),
            "commentNeg": df_negatives.to_dict("records")
        }
        result = Response(json.dumps(output), mimetype='application/json')
        return result
        
api.add_resource(Vnexpress, '/vnexpress') # Route_1

if __name__ == '__main__':
     app.run()
    # print(Tag.objects(idTag='98284'))
