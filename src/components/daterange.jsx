import React from "react";
import moment from "moment";
require("daterangepicker");
require("daterangepicker/daterangepicker-bs3.css");


var Daterange = React.createClass({
    componentDidMount(){
        var start = moment().subtract(29, 'days');
        var end = moment();

        function cb(start, end) {
            $('#dateRange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        }
        $('#dateRange').daterangepicker({
            startDate: start,
            endDate: end,
            ranges: {
                'Today': [moment(), moment()],
                'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                'This Month': [moment().startOf('month'), moment().endOf('month')],
                'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            }
        }, cb);

        cb(start, end);
    },
    render() {
        return (
            <div id="dateRange" className="pull-left" style={{background:"#fff",cursor:"pointer",padding:" 5px 10px", border:" 1px solid #ccc"}}>
                <i className="glyphicon glyphicon-calendar fa fa-calendar"></i>&nbsp;<span></span> <b className="caret"></b>
            </div>
        )
    }
});

export default Daterange
