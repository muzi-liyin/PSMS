import React from "react";
import Daterange from "./daterange"

var Welcome = React.createClass({
    render:function () {
        return <div className="box-center">
            <h5>Welcome</h5>
            <div className="col-lg-4">
                <Daterange />
            </div>
        </div>
    }
});
export default  Welcome;