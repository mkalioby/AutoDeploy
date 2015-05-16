/**
 * Created by mohamed on 15/05/15.
 */

function checkServers(servers)
{
    html='<table class="paleblue">'
    html+='<tr><th>Sever</th><th>Status</th></tr>'
    for (server in servers) {

        html += "<tr><td>" + server + "</td>"

        if (servers[server] == "UP")
            html += '<td><div class="alert alert-success">OK</div> </td>'
        else
            html += '<td><div class="alert alert-danger">Offline</div> </td>'

        html += "</tr>"
    }
    html+='</table>'
    $("#content").html(html)
    }


function clone(data) {
    html=""
    console.log(data)
    if (data == "Done")
        html = "<div class='alert alert-success'>Cloning is succesful</div>"
    else
        html = "<div class='alert alert-danger'>" + data + "</div>"


    $("#content").html(html)
}