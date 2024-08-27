const AWS = require('aws-sdk');
const utils = require('utils');

AWS.config.update({region: 'eu-north-1'});

const dynamodb = new AWS.DynamoDB.DocumentClient();

const tradeTable = 'trade-log';

//------------mainfunction--------------
async function getTradeLog(){
    const params = {
        TableName: tradeTable,
        ProjectionExpression: "dayID, energyBought, energySold, earnings"
    };

    try {
        const data = await dynamodb.scan(params).promise();
        if (!data) {
            return utils.buildResponse(503, 'Error getting trade log');
        } else {
            return utils.buildResponse(200, data.Items);
        }
    } catch (error) {
        console.error('Error getting trade log: ', error);
        return utils.buildResponse(500, 'Error getting trade log');
    }
}

async function addTradeLog(tradeLogInfo){
    const dayID = tradeLogInfo.dayID;
    const energyBought = tradeLogInfo.energyBought;
    const energySold = tradeLogInfo.energySold;
    const earnings = tradeLogInfo.earnings;
    const addedAt = Math.floor(Date.now() / 1000);
    const expiresAt = addedAt + (500 * 60);
    // 500 minutes for expire time

    if (typeof dayID !== 'number' || typeof energyBought !== 'number' || typeof energySold !== 'number' || typeof earnings !== 'number') {
        return utils.buildResponse(401, 'Invalid trade log');
    }

    // if (dayID < 0 || !earnings) {
    //     return utils.buildResponse(401, 'Invalid trade log');
    // }

    const params = {
        TableName: tradeTable,
        Item: {
            dayID: dayID,
            energyBought: Math.round(energyBought * 100) / 100,
            energySold: Math.round(energySold * 100) / 100,
            earnings: Math.round(earnings * 100) / 100,
            addedAt: addedAt,
            expiresAt: expiresAt
        }
    };
    try {
        await dynamodb.put(params).promise();
        return utils.buildResponse(200, 'Trade log added');
    } catch (error) {
        console.error('Error adding trade log: ', error);
        return utils.buildResponse(500, 'Error adding trade log');
    }
}

module.exports = {
    addTradeLog,
    getTradeLog
};