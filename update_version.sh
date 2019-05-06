# This script reads the VERSION file and updates the version in the backend and frontend.
# Don't forget to update the version!!

version="$(cat VERSION)"
 
### Trim leading whitespaces ###
version="${version##*( )}"
  
### trim trailing whitespaces  ##
version="${version%%*( )}"

echo "Updating version to $version"

sed -i "s/current_version = .*/current_version = $version/g" ./backend/app/api/resources.py

sed -i "s/EvergreenDB FSS Version.*/EvergreenDB FSS Version $version/g" ./fss/src/app/settings/settings-page.component.html
