import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("🍽️ Recipe Details")

recipe_id = st.session_state.get("selected_recipe_id")

if recipe_id is None:
    st.error("No recipe selected")
    if st.button("⬅️ Go Back"):
        st.switch_page("pages/11_Browse_Recipes.py")
else:
    try:
        recipe_resp = requests.get(f"http://web-api:4000/r/recipes/{recipe_id}")
        
        if recipe_resp.status_code == 200:
            recipe = recipe_resp.json()
            
            # Display recipe header
            st.header(recipe['name'])
            st.write(f"*Recipe ID: {recipe['recipeID']}*")
            st.write("---")
            
            # Two column layout for main info
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("📋 Description")
                st.write(recipe.get('description', 'No description provided'))
                
                st.write("")
                st.subheader("👨‍🍳 Cooking Instructions")
                steps_text = recipe.get('steps', 'No steps provided')
                # Split steps by newline or number patterns for better display
                st.write(steps_text)
            
            with col2:
                st.subheader("Recipe Info")
                
                # Difficulty rating
                difficulty = recipe.get('difficulty', 3)
                st.write(f"**Difficulty:** {'⭐' * difficulty} ({difficulty}/5)")
                
                # Category
                try:
                    cat_resp = requests.get(f"http://web-api:4000/cat/categories/{recipe['catID']}")
                    if cat_resp.status_code == 200:
                        category = cat_resp.json()
                        st.write(f"**Category:** {category['name']}")
                    else:
                        st.write(f"**Category ID:** {recipe['catID']}")
                except:
                    st.write(f"**Category ID:** {recipe['catID']}")
                
                # Creator
                try:
                    user_resp = requests.get(f"http://web-api:4000/u/users/{recipe['userID']}")
                    if user_resp.status_code == 200:
                        creator = user_resp.json()
                        username = creator.get('username', f"User {recipe['userID']}")
                        st.write(f"**Created by:** {username}")
                    else:
                        st.write(f"**Created by:** User {recipe['userID']}")
                except:
                    st.write(f"**Created by:** User {recipe['userID']}")
                
                st.write("")
                
                # Get and display ratings
                try:
                    ratings_resp = requests.get(f"http://web-api:4000/rat/ratings/recipe/{recipe_id}")
                    if ratings_resp.status_code == 200:
                        ratings = ratings_resp.json()
                        if ratings and len(ratings) > 0:
                            avg_rating = sum(r['rating'] for r in ratings) / len(ratings)
                            st.metric("Average Rating", f"{avg_rating:.1f} ⭐")
                            st.caption(f"Based on {len(ratings)} rating(s)")
                        else:
                            st.info("No ratings yet")
                except:
                    st.info("Ratings unavailable")
            
            st.write("---")
            
            # Ingredients section
            st.subheader("🥕 Ingredients")
            try:
                ing_resp = requests.get(f"http://web-api:4000/r/recipes/{recipe_id}/ingredients")
                if ing_resp.status_code == 200:
                    ingredients = ing_resp.json()
                    if ingredients and len(ingredients) > 0:
                        # Display in columns for better layout
                        ing_cols = st.columns(3)
                        for idx, ing in enumerate(ingredients):
                            with ing_cols[idx % 3]:
                                st.write(f"• {ing.get('name', 'Unknown ingredient')}")
                    else:
                        st.info("No ingredients listed for this recipe")
                else:
                    st.info("Could not load ingredients")
            except:
                st.info("Could not load ingredients")
            
            st.write("---")
            
            # Tags section
            st.subheader("🏷️ Tags")
            try:
                tags_resp = requests.get(f"http://web-api:4000/r/recipes/{recipe_id}/tags")
                if tags_resp.status_code == 200:
                    tags = tags_resp.json()
                    if tags and len(tags) > 0:
                        tag_names = [f"**{tag.get('name', '')}**" for tag in tags]
                        st.write(" • ".join(tag_names))
                    else:
                        st.info("No tags assigned")
                else:
                    st.info("Could not load tags")
            except:
                st.info("Could not load tags")
            
            st.write("---")
            
            # Rate & Review Section
            current_user_id = st.session_state.get("user_id")
            if current_user_id:
                st.subheader("⭐ Rate & Review This Recipe")
                
                with st.form("rate_review_form"):
                    # Rating slider
                    quick_rating = st.slider("Your Rating", min_value=1, max_value=5, value=3, help="Rate from 1 to 5 stars")
                    
                    # Review text area
                    review_text = st.text_area(
                        "Write a Review (optional)", 
                        placeholder="Share your thoughts about this recipe...", 
                        height=100
                    )
                    
                    # Submit button
                    submit_button = st.form_submit_button("Submit Rating & Review", type="primary", use_container_width=True)
                    
                    if submit_button:
                        success_messages = []
                        error_messages = []
                        
                        # Submit rating
                        rating_data = {
                            "recipeID": recipe_id,
                            "userID": current_user_id,
                            "rating": quick_rating
                        }
                        
                        try:
                            rating_resp = requests.post("http://web-api:4000/rat/ratings", json=rating_data)
                            if rating_resp.status_code == 201:
                                success_messages.append(f"✅ Rated {quick_rating} stars!")
                            else:
                                error_messages.append("Could not submit rating. You may have already rated this recipe.")
                        except:
                            error_messages.append("Error submitting rating")
                        
                        # Submit review if provided
                        if review_text and review_text.strip():
                            review_data = {
                                "recipeID": recipe_id,
                                "userID": current_user_id,
                                "review": review_text.strip()
                            }
                            
                            try:
                                review_resp = requests.post("http://web-api:4000/rev/reviews", json=review_data)
                                if review_resp.status_code == 201:
                                    success_messages.append("✅ Review submitted!")
                                else:
                                    error_messages.append("Could not submit review. You may have already reviewed this recipe.")
                            except:
                                error_messages.append("Error submitting review")
                        
                        # Display messages
                        for msg in success_messages:
                            st.success(msg)
                        for msg in error_messages:
                            st.error(msg)
                        
                        if success_messages:
                            st.rerun()
            
            st.write("---")
            
            # Reviews section
            st.subheader("💬 User Reviews")
            try:
                reviews_resp = requests.get(f"http://web-api:4000/rev/reviews/recipe/{recipe_id}")
                if reviews_resp.status_code == 200:
                    reviews = reviews_resp.json()
                    if reviews and len(reviews) > 0:
                        for review in reviews:
                            with st.container(border=True):
                                # Get username if possible
                                try:
                                    user_resp = requests.get(f"http://web-api:4000/u/users/{review['userID']}")
                                    if user_resp.status_code == 200:
                                        user = user_resp.json()
                                        username = user.get('username', f"User {review['userID']}")
                                    else:
                                        username = f"User {review['userID']}"
                                except:
                                    username = f"User {review['userID']}"
                                
                                st.write(f"**{username}:**")
                                st.write(review.get('review', 'No review text'))
                    else:
                        st.info("No reviews yet. Be the first to review this recipe!")
                else:
                    st.info("Could not load reviews")
            except:
                st.info("Could not load reviews")
            
        else:
            st.error("Recipe not found or could not be loaded")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        st.info("Please ensure the API server is running")

# Navigation buttons
st.write("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Back to Browse", use_container_width=True):
        st.switch_page("pages/10_Recipe_Browser_Home.py")

with col2:
    # Add to collection button
    current_user_id = st.session_state.get("user_id")
    if current_user_id and st.button("➕ Save to Collection", use_container_width=True):
        # Could implement a quick "add to collection" modal here
        st.info("Go to 'My Collections' to add this recipe to a collection")