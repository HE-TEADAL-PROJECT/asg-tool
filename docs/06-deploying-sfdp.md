# Deploying the ASG

After SFDP is generated and validated, it can be deployed to a TEADAL Node. For that we need to 

1. Create a TEADAL Gitlab repository to hold this new data application. 
First, create new repository in `gitlab.teadal.ubiwhere.com` server, in one of TEADAL groups, say `<teadal-group-name>`, named as `<sfdp-repo-name>`. 
Next, upload the validated SFDP app to this new repository:
```sh
git init --initial-branch=main
git remote add origin git@gitlab.teadal.ubiwhere.com:<teadal-group-name>/sfdp-repo-name>.git
git add .
git commit -m "Initial commit"
git push --set-upstream origin main
```
After the project is pudhed sucessfully, new SFDP app image is created and pushed to image repository of the TEADAL Gitlab Group, <teadal-group-name>` .

2. Create policies required for this app to be accessed as planned by the FDP-to-SFDP contracts.
TODO - point to instructions on achieving this goal (outside of the ASG sybsystem scope).

3. Create deployement manifests required for this app to be picked up by the argocd daemon on the target TEADAL Node.
TODO - point to instructions on achieving this goal (outside of the ASG sybsystem scope).

After deployment manifests and policy files are pushed to the argocd repo of the target TEADAL Node, the app should be picked up by the target argocd daemon and become available for SFDP users. 