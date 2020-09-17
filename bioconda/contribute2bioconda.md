# 0. Release a stable version of your software  
     process on you github page  
# 1. Create a Fork of our Recipes Repo  
     on https://github.com/bioconda/bioconda-recipes 
# 2. Create Local “Clone”  
     git clone https://github.com/<USERNAME>/bioconda-recipes.git
     cd bioconda-recipes
     git remote add upstream https://github.com/bioconda/bioconda-recipes.git  
     
# 3. Contribute to the BIOCONDA
## 3.1 Create a Branch


    # Make sure our master is up to date with Bioconda
    git checkout master
    git pull upstream master
    git push origin master
    
    # Create and checkout a new branch for our work
    git checkout -b update_my_recipe  
    
## 3.2 Make Some Edits

    # Choose the edited files to commit:
    git add pyaml
    # Create a commit (will open editor)
    git commit
    # Push your commit to GitHub
    git push
## 3.3. Push Changes

    # Choose the edited files to commit:
    git add pyaml
    # Create a commit (will open editor)
    git commit
    # Push your commit to GitHub
    git push


## 3.4. Create a Pull Request

## 3.5. Delete your Branch
    
    # Delete local branch
    git branch -D my_branch
    # Delete branch in your fork via the remote named "origin"
    git push origin -d my_branch