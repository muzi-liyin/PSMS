/**
 * Created by sa on 16-12-20.
 */
let location_hostname = location.hostname;
let url="";
if(location_hostname.includes("localhost")>-1 || location_hostname.includes("35.161.236.80")>-1 ){
    url = "http://35.161.236.80:5100";
}else {
    url = "";
}
const config = {
    url:url
};
module.exports = {
    config:config
};