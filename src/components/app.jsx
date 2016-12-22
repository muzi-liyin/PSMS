import React from "react";
var App = React.createClass({
    getInitialState(){
        return {
            opacity:1.0
        }
    },
    componentWillMount(){
        console.log("在渲染前调用,在客户端也在服务端。"+ this.state.opacity)
    },
    componentWillReceiveProps(){
        console.log("点击切换路由可以写这里");
    },
    componentDidMount(){
        return;
        this.props.router.setRouteLeaveHook(
            this.props.route,
            this.routerWillLeave
        )
        this.timer = setInterval(function () {
            var opacity = this.state.opacity;
            opacity -=0.05;
            if(opacity<0.1){
                opacity = 1.0;
            }
            this.setState({
                opacity:opacity
            })
        }.bind(this),100);
    },
    render:function () {
        return <div className="container-fluid">{this.props.children}</div>
    }
});
module.exports = App;
