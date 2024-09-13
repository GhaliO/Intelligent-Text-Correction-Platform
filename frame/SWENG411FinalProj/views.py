from django.shortcuts import render
from django.http import JsonResponse
from .spelling_corrector import correct_text_generic  # Import your spelling correction function

def index(request):
    return render(request, 'Text Correction Screen.html')  # Use the appropriate path to your HTML template

def correct_text(request):
    if request.method == "POST":
        print("correct_text view accessed")
        data = request.POST.get("text", "")
        corrected_text = correct_text_generic(data)
        return JsonResponse({"corrected_text": corrected_text})