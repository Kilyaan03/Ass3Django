from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from .forms import ReviewForm, CommentForm, RegisterForm, UserProfileForm
from .models import Review, Comment
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import login, authenticate

# Create your views here.

# This is a simple view that returns a plain text response.
def home(request):
    return HttpResponse("Hello Test works!")

@login_required
def create_review(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Only staff members can create reviews.")

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'myapp/create_review.html', {'form': form})

@login_required
def update_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'myapp/update_review.html', {'form': form})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    # Optional: prevent users from deleting others' reviews
    if review.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to delete this review.")

    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    
    return render(request, 'myapp/delete_review.html', {'review': review})

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'myapp/review_list.html', {'reviews': reviews})

@login_required
def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    comments = Comment.objects.filter(review=review)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
            return redirect('myapp/review_detail.html', review_id=review.id)
    else:
        form = CommentForm()

    return render(request, 'myapp/review_detail.html', {
        'review': review,
        'form': form,
        'comments': comments
    })

def review_comments_json(request, review_id):
    """
    This function gets all the comments for a specific review and sends them back as JSON.
    - First, it finds the review using the review_id. If it doesn’t exist, it shows a 404 error.
    - Then, it grabs all the comments for that review and sorts them by the newest ones first.
    - After that, it converts the comments into a list of dictionaries with the username, text, and date.
    - Finally, it sends the list back as a JSON response.

    Why: This is super useful for loading comments dynamically on the frontend without refreshing the page.
    """
    review = get_object_or_404(Review, pk=review_id)  # Look for the review. If it’s not there, show a 404 error.
    comments = Comment.objects.filter(review=review).order_by('-created_at')  # Get all comments for the review, newest first.
    comment_list = list(comments.values('user__username', 'text', 'created_at'))  # Turn the comments into a list of dictionaries.
    return JsonResponse({'comments': comment_list})  # Send the list as JSON so the frontend can use it.


@csrf_exempt  # This skips CSRF checks (not safe for production, but okay for testing).
@login_required  # Only logged-in users can use this function.
def add_comment_ajax(request, review_id):
    """
    This function lets users add a new comment to a review using AJAX.
    - It only works if the request is a POST request.
    - It expects the comment text to be sent in JSON format.
    - It checks if the comment is valid (e.g., not too short).
    - If valid, it creates a new comment linked to the review and the user.
    - Then, it sends back a success message with the new comment details or an error if something went wrong.

    Why: This makes it easier for users to add comments without refreshing the page.
    """
    if request.method == 'POST':  # Make sure it’s a POST request.
        try:
            data = json.loads(request.body)  # Get the JSON data from the request body.
            text = data.get('text')  # Extract the comment text.

            # Check if the comment text is valid.
            if not text or len(text.strip()) < 3:  # If the comment is empty or too short, show an error.
                return JsonResponse({'error': 'Comment too short'}, status=400)

            # Find the review. If it doesn’t exist, show a 404 error.
            review = get_object_or_404(Review, pk=review_id)

            # Create a new comment and link it to the review and the logged-in user.
            comment = Comment.objects.create(
                review=review,
                user=request.user,
                text=text
            )

            # Send back a success response with the new comment details.
            return JsonResponse({
                'success': True,
                'comment': {
                    'user': request.user.username,  # The username of the person who wrote the comment.
                    'text': comment.text,  # The actual comment text.
                    'created_at': str(comment.created_at)  # When the comment was created.
                }
            })
        except Exception as e:
            # If something unexpected happens, send back an error message.
            return JsonResponse({'error': str(e)}, status=400)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('review_list')
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})
