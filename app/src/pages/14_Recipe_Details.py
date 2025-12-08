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
        # GET specific recipe details
        recipe_resp = requests.get(f"http://web-api:4000/r/recipes/{recipe_id}")
        
        if recipe_resp.status_code == 200:
            recipe = recipe_resp.json()
            
            # Display recipe header
            st.header(recipe['name'])
            st.write(f"*Recipe ID: {recipe['recipeID']}*")
            st.write("---")
            
            # Two column layout
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("📋 Description")
                st.write(recipe.get('description', 'No description provided'))
                
                st.subheader("👨‍🍳 Cooking Instructions")
                st.write(recipe.get('steps', 'No steps provided'))
            
            with col2:
                st.subheader("Details")
                st.write(f"**Difficulty:** {'⭐' * recipe['difficulty']} ({recipe['difficulty']}/5)")
                st.write(f"**Category ID:** {recipe['catID']}")
                st.write(f"**Created by User:** {recipe['userID']}")
                
                # Get and display average rating
                try:
                    ratings_resp = requests.get(f"http://web-api:4000/rat/ratings/recipe/{recipe_id}")
                    if ratings_resp.status_code == 200:
                        ratings = ratings_resp.json()
                        if ratings:
                            avg_rating = sum(r['rating'] for r in ratings) / len(ratings)
                            st.metric("Average Rating", f"{avg_rating:.1f} ⭐", delta=f"{len(ratings)} ratings")
                        else:
                            st.info("No ratings yet")
                except:
                    pass
            
            st.write("---")
            
            # Ingredients section
            st.subheader("🥕 Ingredients")
            try:
                ing_resp = requests.get(f"http://web-api:4000/r/recipes/{recipe_id}/ingredients")
                if ing_resp.status_code == 200:
                    ingredients = ing_resp.json()
                    if ingredients:
                        for ing in ingredients:
                            st.write(f"- {ing.get('name', 'Unknown ingredient')}")
                    else:
                        st.info("No ingredients listed")
            except:
                st.info("Could not load ingredients")
            
            st.write("---")
            
            # Tags section
            st.subheader("🏷️ Tags")
            try:
                tags_resp = requests.get(f"http://web-api:4000/r/recipes/{recipe_id}/tags")
                if tags_resp.status_code == 200:
                    tags = tags_resp.json()
                    if tags:
                        tag_names = [tag.get('name', '') for tag in tags]
                        st.write(" • ".join(tag_names))
                    else:
                        st.info("No tags")
            except:
                st.info("Could not load tags")
            
            st.write("---")
            
            # Reviews section
            st.subheader("💬 Reviews")
            try:
                reviews_resp = requests.get(f"http://web-api:4000/rev/reviews/recipe/{recipe_id}")
                if reviews_resp.status_code == 200:
                    reviews = reviews_resp.json()
                    if reviews:
                        for review in reviews:
                            with st.container(border=True):
                                st.write(f"**User {review['userID']}:**")
                                st.write(review['review'])
                    else:
                        st.info("No reviews yet. Be the first to review!")
            except:
                st.info("Could not load reviews")
        
        else:
            st.error("Recipe not found")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {str(e)}")

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Back to Browse", use_container_width=True):
        st.switch_page("pages/11_Browse_Recipes.py")

with col2:
    if st.button("⭐ Rate This Recipe", type="primary", use_container_width=True):
        st.switch_page("pages/12_Rate_Review.py")