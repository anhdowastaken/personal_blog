import Vue from 'vue'

export const EventBus = new Vue()

export function isValidJwt (jwt) {  
    if (!jwt || jwt.split('.').length < 3) {
        return false
    }
    
    const data = JSON.parse(atob(jwt.split('.')[1]))
    const exp = new Date(data.exp * 1000) // JS deals with dates in milliseconds since epoch
    const now = new Date()
    
    return now < exp
}

export function isEmpty(obj) {
    for(var prop in obj) {
        if(obj.hasOwnProperty(prop))
        return false;
    }
    
    return JSON.stringify(obj) === JSON.stringify({});
}

export function msToTime(ms, day=true, hour=true, min=true, sec=false) {
    if (ms < 0) {
        return ''
    }

    let msecs = ms % 1000;
    ms = (ms - msecs) / 1000;
    let secs = ms % 60;
    ms = (ms - secs) / 60;
    let mins = ms % 60;
    ms = (ms - mins) / 60
    let hrs = ms % 24;
    let days = (ms - hrs) / 24
    
    return (days && day ? days + 'd' : '')
           + (hrs && hour ? hrs + 'h' : '')
           + (mins && min ? mins + 'm' : '')
           + (secs && sec ? secs + 's' : '')
}

