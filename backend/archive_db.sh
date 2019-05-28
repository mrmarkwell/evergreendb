date=`date +%b_%d_%Y_%H_%M_%S`
mkdir -p db_archives
if [ -f fss.db ]; then
    mv fss.db "db_archives/fss_$date.db"
fi
if [ -f soar.db ]; then
    mv soar.db "db_archives/soar_$date.db"
fi
if [ -d app/static/photos ]; then
    mkdir -p db_archives/static_$date
    mv app/static/photos "db_archives/static_$date/photos"
fi
if [ -d app/static/medical ]; then
    mkdir -p db_archives/static_$date
    mv app/static/medical "db_archives/static_$date/medical"
fi
if [ -d app/static/interactions ]; then
    mkdir -p db_archives/static_$date
    mv app/static/interactions "db_archives/static_$date/interactions"
fi
