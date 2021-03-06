from upload_data.decorator import is_superuser
from handle_sentence.models import Sentence
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd

# Create your views here.


class UploadSentences(APIView):
    @is_superuser
    def post(self, *args, **kwargs):
        request = self.request
        try:
            file = request.FILES["file"]
            filetype = request.data.get("filetype", None)
            df = None
            if filetype == "xlsx":
                df = pd.read_excel(file.read())
            elif not filetype or filetype == "csv":
                df = pd.read_csv(file)
            Sentence.objects.bulk_create(
                [
                    Sentence(sentence=single_sentence)
                    for single_sentence in df["sentence"]
                ]
            )
            return Response({"details": "saved"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"details": e.__repr__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
