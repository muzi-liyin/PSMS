import React from "react";
import {ajax} from "../lib/ajax";
import {valid,setForm,getForm} from "../lib/form";

var CreateCustomer = React.createClass({
    submit(){
        if(valid("#create_customer","data-required")){
            console.log(JSON.stringify(setForm("#create_customer","data-key")))
            return;
            ajax("get","https://api.github.com/search/repositories?q="+"10",null,function (data) {
                console.log(data)
            });
        }else {
            $(".has-error input:first").focus();
        }
        /*<p>{this.props.params.name}</p>*/
    },
    componentDidMount(){
      var data ={"company":{"name":"名称","address":"地址","select":"2"},"radio":"2","remark":"备注"};
      getForm("#create_customer",data)
    },
    render:function () {
        return (
            <div className="col-sm-6 col-sm-offset-3 animated slideInDown create_customer">
                <form id="create_customer" className="form-horizontal" role="form" noValidate="noValidate">
                    <div className="form-group">
                        <label htmlFor="company_name" className="col-sm-2 control-label text-right">* 公司名称</label>
                        <div className="col-sm-10">
                            <input type="text" data-required="true" data-key="company.name"  name="name" className="form-control" id="company_name"  placeholder="Name" />
                            <p className="none red">名称必须跟Invoice公司名称一致</p>
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="company_address" className="col-sm-2 control-label text-right">* 公司地址</label>
                        <div className="col-sm-10">
                            <input  type="text" data-required="true"　data-key="company.address" name="address" className="form-control" id="company_address" placeholder="Address" />
                        </div>
                    </div>

                    <div className="form-group">
                        <label htmlFor="company_address" className="col-sm-2 control-label text-right">* select</label>
                        <div className="col-sm-10">
                           <select className="form-control" 　data-required="true" data-key="company.select">
                               <option value=''>1</option>
                               <option value={1}>1</option>
                               <option value={2}>2</option>
                           </select>
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="company_address" className="col-sm-2 control-label text-right">* radio</label>
                        <div className="col-sm-10">
                            <input  type="radio"　data-required="true" data-key="radio" name="radio" value={1}/>1
                            <input  type="radio" data-required="true" data-key="radio" name="radio" value={2}/>2
                            <input  type="radio" data-required="true" data-key="radio" name="radio" value=''/>2

                        </div>
                    </div>


                    <div className="form-group">
                        <label htmlFor="company_remark" className="col-sm-2 control-label text-right">备注</label>
                        <div className="col-sm-10">
                            <textarea className="form-control" data-key="remark" name="remark" id="company_remark">

                            </textarea>
                        </div>
                    </div>
                    <div className="form-group">
                        <div className="col-sm-offset-2 col-sm-10">
                            <button onClick={this.submit} type="button" className="btn btn-primary">Create/Update</button>
                            <button type="button" className="btn btn-warning" style={{marginLeft:"20px"}}>Cancel</button>
                        </div>
                    </div>
                </form>
            </div>
        )
    }
});
export default  CreateCustomer;
