import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("🔎 Browse All Recipes")

# Filters section
st.write("### Filter Recipes")

col1, col2, col3 = st.columns(3)

# Get filter options from API
categories = []
tags = []

try:
    cat_response = requests.get("http://web-api:4000/cat/categories")
    if cat_response.status_code == 200:
        categories = cat_response.json()
except:
    pass

try:
    tag_response = requests.get("http://web-api:4000/tag/tags")
    if tag_response.status_code == 200:
        tags = tag_response.json()
except:
    pass

with col1:
    if categories:
        category_options = ["All Categories"] + [cat['name'] for cat in categories]
        selected_category = st.selectbox("Category", category_options)
    else:
        selected_category = "All Categories"

with col2:
    difficulty_filter = st.selectbox("Difficulty", ["All", "1", "2", "3", "4", "5"])

with col3:
    if tags:
        tag_options = ["All Tags"] + [tag['name'] for tag in tags]
        selected_tag = st.selectbox("Tag", tag_options)
    else:
        selected_tag = "All Tags"

# Search box
search_term = st.text_input("🔍 Search recipes by name", placeholder="Enter recipe name...")

st.write("---")

# Fetch and display recipes
try:
    # GET all recipes
    response = requests.get("http://web-api:4000/r/recipes")
    
    if response.status_code == 200:
        all_recipes = response.json()
        
        # Apply filters
        filtered_recipes = all_recipes
        
        # Filter by search term
        if search_term:
            filtered_recipes = [r for r in filtered_recipes if search_term.lower() in r['name'].lower()]
        
        # Filter by difficulty
        if difficulty_filter != "All":
            filtered_recipes = [r for r in filtered_recipes if r['difficulty'] == int(difficulty_filter)]
        
        # Filter by category (would need to match catID with category name)
        if selected_category != "All Categories" and categories:
            cat_id = next((cat['catID'] for cat in categories if cat['name'] == selected_category), None)
            if cat_id:
                filtered_recipes = [r for r in filtered_recipes if r['catID'] == cat_id]
        
        # Display count
        st.write(f"### Found **{len(filtered_recipes)}** recipe(s)")
        
        if len(filtered_recipes) == 0:
            st.info("No recipes match your filters. Try adjusting your search criteria.")
        else:
            # Display recipes in a grid-like format
            for i in range(0, len(filtered_recipes), 2):
                cols = st.columns(2)
                
                for j, col in enumerate(cols):
                    if i + j < len(filtered_recipes):
                        recipe = filtered_recipes[i + j]
                        
                        with col:
                            with st.container(border=True):
                                st.subheader(f"🍽️ {recipe['name']}")
                                st.write(f"**Difficulty:** {'⭐' * recipe['difficulty']}")
                                st.write(f"**Description:** {recipe.get('description', 'No description')[:100]}...")
                                
                                # Get average rating
                                try:
                                    ratings_resp = requests.get(f"http://web-api:4000/rat/ratings/recipe/{recipe['recipeID']}")
                                    if ratings_resp.status_code == 200:
                                        ratings = ratings_resp.json()
                                        if ratings:
                                            avg_rating = sum(r['rating'] for r in ratings) / len(ratings)
                                            st.write(f"**Rating:** {avg_rating:.1f} ⭐ ({len(ratings)} reviews)")
                                        else:
                                            st.write("**Rating:** No ratings yet")
                                except:
                                    pass
                                
                                # View details button
                                if st.button("View Details", key=f"view_{recipe['recipeID']}", use_container_width=True):
                                    st.session_state["selected_recipe_id"] = recipe["recipeID"]
                                    st.session_state["selected_recipe"] = recipe
                                    st.switch_page("pages/14_Recipe_Details.py")
    
    else:
        st.error("Failed to fetch recipes")

except requests.exceptions.RequestException as e:
    st.error(f"Error: {str(e)}")

# Navigation
if st.button("⬅️ Back to Home", use_container_width=True):
    st.switch_page("Home.py")