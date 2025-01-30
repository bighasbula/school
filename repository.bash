git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/bighasbula/school.git
git branch -M main
git push -u origin main
git add cloudbuild.yaml
git commit -m "Add Cloud Build configuration"
git push origin main