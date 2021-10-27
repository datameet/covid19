rm ../../data/data.sqlite
cat ../../data/mohfw_vaccination_status.json | jq [.rows[].value] | sqlite-utils insert ../../data/data.sqlite covid19_vaccinations - --pk=_id
cat ../../data/mohfw.json | jq [.rows[].value] | sqlite-utils insert ../../data/data.sqlite covid19_cases - --pk=_id
cat ../../data/communal_incidents.json | jq [.rows[].value] | sqlite-utils insert ../../data/data.sqlite covid19_communal_incidents - --pk=_id
cat ../../data/non_virus_deaths.json | jq [.rows[].value] | sqlite-utils insert ../../data/data.sqlite covid19_non_virus_deaths - --pk=_id
cat ../../data/icmr_testing_status.json | jq [.rows[].value] | sqlite-utils insert ../../data/data.sqlite covid19_tests - --pk=_id
