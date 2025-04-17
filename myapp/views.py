from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from .forms import ReviewForm, CommentForm, RegisterForm
from .models import Review, Comment
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth import login

# This is a simple view that returns a plain text response.
# It's mainly used to test if the server is running correctly.
def home(request):
    return HttpResponse("Hello Test works!")

# View for creating a review.
# Only staff members can access this view, and it requires the user to be logged in.
@login_required
def create_review(request):
    if not request.user.is_staff:
        # If the user is not a staff member, they are forbidden from accessing this view.
        return HttpResponseForbidden("Only staff members can create reviews.")

    if request.method == 'POST':
        # If the form is submitted, validate the data.
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Save the review but don't commit yet so can add the author.
            review = form.save(commit=False)
            review.author = request.user  # Set the current user as the author.
            review.save()  # Save the review to the database.
            return redirect('review_list')  # Redirect to the review list page.
    else:
        # If the request is not POST, display an empty form.
        form = ReviewForm()
    return render(request, 'myapp/create_review.html', {'form': form})

# View for updating an existing review.
@login_required
def update_review(request, review_id):
    # Get the review by its ID or return a 404 error if it doesn't exist.
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        # If the form is submitted, validate and save the updated data.
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()  # Save the updated review.
            return redirect('review_list')  # Redirect to the review list page.
    else:
        # If the request is not POST, display the form with the current review data.
        form = ReviewForm(instance=review)
    return render(request, 'myapp/update_review.html', {'form': form})

# View for deleting a review.
@login_required
def delete_review(request, review_id):
    # Get the review by its ID or return a 404 error if it doesn't exist.
    review = get_object_or_404(Review, pk=review_id)

    # Optional: Prevent users from deleting reviews they don't own unless they are staff.
    if review.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to delete this review.")

    if request.method == 'POST':
        # If the form is submitted, delete the review and redirect to the review list.
        review.delete()
        return redirect('review_list')
    
    # Render a confirmation page before deleting.
    return render(request, 'myapp/delete_review.html', {'review': review})

# View for listing all reviews.
def review_list(request):
    # Get all reviews from the database.
    reviews = Review.objects.all()
    return render(request, 'myapp/review_list.html', {'reviews': reviews})

# View for displaying the details of a specific review.

def review_detail(request, review_id):
    # Get the review by its ID or return a 404 error if it doesn't exist.
    review = get_object_or_404(Review, pk=review_id)
    # Get all comments related to this review.
    comments = Comment.objects.filter(review=review)

    if request.method == 'POST':
        # If the form is submitted, validate and save the comment.
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review  # Link the comment to the review.
            comment.user = request.user  # Set the current user as the author of the comment.
            comment.save()
            return redirect('myapp/review_detail.html', review_id=review.id)
    else:
        # If the request is not POST, display an empty comment form.
        form = CommentForm()

    return render(request, 'myapp/review_detail.html', {
        'review': review,
        'form': form,
        'comments': comments
    })

# View for returning all comments for a specific review as JSON.
def review_comments_json(request, review_id):
    """
    This function gets all the comments for a specific review and sends them back as JSON.
    - Useful for dynamically loading comments on the frontend without refreshing the page.
    """
    review = get_object_or_404(Review, pk=review_id)  # Get the review or return a 404 error.
    comments = Comment.objects.filter(review=review).order_by('-created_at')  # Get all comments, newest first.
    comment_list = list(comments.values('user__username', 'text', 'created_at'))  # Convert comments to a list of dictionaries.
    return JsonResponse({'comments': comment_list})  # Return the comments as JSON.

# View for adding a comment using AJAX.

def add_comment_ajax(request, review_id):
    """
    This function lets users add a new comment to a review using AJAX.
    - Makes the process faster and avoids page reloads.
    """
    if request.method == 'POST':  # Ensure the request is POST.
        try:
            data = json.loads(request.body)  # Parse the JSON data from the request.
            text = data.get('text')  # Extract the comment text.

            # Validate the comment text.
            if not text or len(text.strip()) < 3:  # Check if the comment is too short.
                return JsonResponse({'error': 'Comment too short'}, status=400)

            # Get the review or return a 404 error.
            review = get_object_or_404(Review, pk=review_id)

            # Create and save the new comment.
            comment = Comment.objects.create(
                review=review,
                user=request.user,
                text=text
            )

            # Return the new comment details as JSON.
            return JsonResponse({
                'success': True,
                'comment': {
                    'user': request.user.username,
                    'text': comment.text,
                    'created_at': str(comment.created_at)
                }
            })
        except Exception as e:
            # Handle unexpected errors.
            return JsonResponse({'error': str(e)}, status=400)

# View for user registration.
def register(request):
    if request.method == 'POST':
        # If the form is submitted, validate and save the user.
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user.
            login(request, user)  # Log the user in automatically.
            return redirect('review_list')  # Redirect to the review list page.
    else:
        # If the request is not POST, display an empty registration form.
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

# Simple views for rendering static pages.
def index(request):
    reviews = Review.objects.all()  # Fetch all reviews
    return render(request, 'myapp/index.html', {'reviews': reviews})

def archer(request):
    return render(request, 'myapp/Archer.html')

def monk(request):
    return render(request, 'myapp/Monk.html')

def asip(request):
    return render(request, 'myapp/ASIP_Review.html')

def tayto(request):
    return render(request, 'myapp/TaytoPark_Review.html')

def futuroscope(request):
    return render(request, 'myapp/Futuroscope.html')

def Parc_Asterix(request):
    return render(request, 'myapp/Parc_Asterix.html')

def PastaReview(request):
    return render(request, 'myapp/PastaReview.html')

def PizzaReview(request):
    return render(request, 'myapp/PizzaReview.html')

def CroqMonsieur(request):
    return render(request, 'myapp/CroqMonsieur.html')

def base(request):
    return render(request, 'myapp/base.html')
