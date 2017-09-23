mkdir -p db_archives
if [ -f fss.db ]; then
    mv fss.db db_archives/fss_$(date +%b_%d_%Y_%H_%M_%S).db
fi
if [ -f soar.db ]; then
    mv soar.db db_archives/soar_$(date +%b_%d_%Y_%H_%M_%S).db
fi
