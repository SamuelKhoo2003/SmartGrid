// Importing all the services and exporting them to be used in the routes
const accessEnergyLogService = require('./services/accessEnergyLog');
const accessTradeLogService = require('./services/accessTradeLog');
const accessUsageLogService = require('./services/accessUsageLog');
const utils = require('utils');

const accessEnergyLogPath = '/accessEnergyLog';
const accessTradeLogPath = '/accessTradeLog';
const accessUsageLogPath = '/accessUsageLog';

exports.handler = async (event) => {
    console.log('Request Event: ', event);
    let response;
    switch(true) {
        case event.path === accessEnergyLogPath && event.httpMethod === 'GET':
            response = await accessEnergyLogService.getEnergyLog(event);
            break;
        case event.path === accessEnergyLogPath && event.httpMethod === 'POST':
            const energyLogBody = JSON.parse(event.body);
            response = await accessEnergyLogService.addEnergyLog(energyLogBody);
            break;
        case event.path === accessTradeLogPath && event.httpMethod === 'GET':
            response = await accessTradeLogService.getTradeLog(event);
            break;
        case event.path === accessTradeLogPath && event.httpMethod === 'POST':
            const tradeLogBody = JSON.parse(event.body);
            response = await accessTradeLogService.addTradeLog(tradeLogBody);
            break;
        case event.path === accessUsageLogPath && event.httpMethod === 'GET':
            response = await accessUsageLogService.getUsageLog(event);
            break;
        case event.path === accessUsageLogPath && event.httpMethod === 'POST':
            const usageLogBody = JSON.parse(event.body);
            response = await accessUsageLogService.addUsageLog(usageLogBody);
            break;
        default:
            response = utils.buildResponse(404, '404 Not Found');
    }
    return response;
};
