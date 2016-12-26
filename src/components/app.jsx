import React from "react";
import {ajax} from "../lib/ajax";

var App = React.createClass({
    getInitialState(){
        return {
            opacity:1.0
        }
    },
    componentWillUpdate(){
        if(location.hash!="#/login"){
            ajax("post","/api/user/verify_session").then(function (data) {
                var data = JSON.parse(data);
                if(data.code=="200"){
                    $(".userEmail").html(data.results.email);
                    $(".userId").html(data.results.id);
                    $(".isShow").show();
                }else {
                    $(".ajax_error").html(data.message);
                    $(".modal").modal("toggle");
                    $(".userEmail").html("");
                    $(".userId").html("");
                    $(".modal").on("hidden.bs.modal",function () {
                        location.hash="login";
                        $(".isShow").hide();
                    })
                }
            });
        }
        console.log('componentWillUpdate----------')
    },
    componentWillUnmount(){
        console.log('componentWillUnmount--------')
    },
    componentWillMount(){
        console.log("componentWillMount----------")
    },
    componentWillReceiveProps(){
        console.log("componentWillReceiveProps----------------------------");
    },
    componentDidMount(){
        console.log('componentDidMount-----------')
    },
    render:function () {
        return <div className="container-fluid">{this.props.children}</div>
    }
});
module.exports = App;
