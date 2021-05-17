function create_table(tabledata){
    console.log(tabledata);
    console.log("datatable started")
    console.log($('#data_table'))
    $.fn.dataTable.moment( 'DD-MM-YYYY');
    $('#data_table').DataTable( {
        data: tabledata,
        pageLength: 25,
        responsive: true,
        columns: [
            {title:"S.No.", data:"s_no"},
            {title:"Date of Incident", data:"date_of_incident"},
            {title:"Hospital/Place", data:"hospital_place"},
            {title:"District", data:"district"},
            {title:"State", data:"state"},
            {title:"No of Deaths", data:"no_of_deaths"},
            {title:"Category", data:"category"},
            {title: "Source", data:"source", 
                                   "render": function(data, type, row, meta){
                                        if(type === 'display'){
                                            data = data.replace("www.","");
                                            data = data.replace(".com","");
                                            data = data.replace(".in","");
                                            data = data.replace(".net","");
                                            data = '<a  target="_blank" href="' + row['reference'] + '">' + data + '</a>  on '+row['date_of_report'];
                                        }
                                        return data;
                                     }

            }, 
        ]
    } );

console.log("datatable created")

}

function get_data_create_table(){

    d3.csv('https://raw.githubusercontent.com/datameet/covid19/master/data/oxygen_shortage_deaths_in_india.csv')
      .then(function(data) {
          // data is now whole data set
          // draw chart in here!
          create_table(data)
      })
      .catch(function(error){
         // handle error   
      })

}

$( document ).ready(function() {
  get_data_create_table()
});

