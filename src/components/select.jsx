import React from "react";
require("select2");
require("select2/dist/css/select2");
import {ajax} from "../lib/ajax";

var Select = React.createClass({
    componentDidMount(){
        //var data = [{ id: 0, text: 'enhancement' }, { id: 1, text: 'bug' }, { id: 2, text: 'duplicate' }, { id: 3, text: 'invalid' }, { id: 4, text: 'wontfix' }];
        ajax("get",this.props.url,{}).then(function (data) {
            $(".js-example-data-array").select2({
                data: data.data,
                multiple: true
            })
        });
        $(".js-example-data-array").on("change",function () {
            console.log($(this).val())
        });
    },
    render(){
        return (
           <select className="js-example-data-array form-control"> </select>
        )
    }
});

var AjaxSelect = React.createClass({
    componentDidMount(){
        $("."+this.props.className).select2({
            ajax: {
                url: this.props.url, //"https://api.github.com/search/repositories",
                dataType: 'json',
                delay: 500,
                data: function (params) {
                    return {
                        q: params.term
                    };
                },
                processResults: function (data, params) {
                    var data = [{ id: 10, text: 'enhancement' }, { id: 1, text: 'bug' }, { id: 2, text: 'duplicate' }, { id: 3, text: 'invalid' }, { id: 4, text: 'wontfix' }];
                    return {
                        results: data
                    };
                },
                cache: true
            },
            minimumInputLength: 1,
            multiple: this.props.multiple,
            placeholder:this.props.placeholder
        });
    },
    render(){
        return (
            <select  className={this.props.className+" form-control"} > </select>
        )
    }
});

module.exports ={
    Select:Select,
    AjaxSelect:AjaxSelect
}
