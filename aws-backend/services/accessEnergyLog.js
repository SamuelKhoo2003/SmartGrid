// This has now chaned to include the usage log too

const AWS = require('aws-sdk');
const utils = require('utils');

// set the region
AWS.config.update({region: 'eu-north-1'});

// create the dynamodb object
const dynamodb = new AWS.DynamoDB.DocumentClient();

// choose the db table to use
const energyTable = 'energy-log';

//------------mainfunction--------------
async function getEnergyLog() {
    const params = {
        TableName: energyTable,
        ProjectionExpression: 'dayID, energyUsed, energyProduced',
        // Limit: 90,
    };
    const result = await dynamodb.scan(params).promise();
    if (!result) {
        return utils.buildResponse(503, 'Error getting energy log');
    } else {
        return utils.buildResponse(200, result.Items);
    }
}

async function addEnergyLog(energyLogInfo) {
    const dayID = energyLogInfo.dayID;
    const energyUsed = energyLogInfo.energyUsed;
    const energyProduced = energyLogInfo.energyProduced;
    const addedAt = Math.floor(Date.now() / 1000);
    const expiresAt = addedAt + (500 * 60);

    // if (!dayID || !avgSunIrradiance || !energyProduced) {
    //     return utils.buildResponse(401, 'Invalid energy log');
    // }

    if (typeof dayID !== 'number' || typeof energyUsed !== 'number' || typeof energyProduced !== 'number') {
        return utils.buildResponse(401, 'Invalid energy log');
    }
    const params = {
        TableName: energyTable,
        Item: {
            dayID: dayID,
            energyUsed: Math.round(energyUsed * 100) / 100,
            energyProduced: Math.round(energyProduced * 100) / 100,
            addedAt: addedAt,
            expiresAt: expiresAt
        }
    };

    try {
        await dynamodb.put(params).promise();
        return utils.buildResponse(200, 'Energy log added');
    } catch (error) {
        console.error('Error adding energy log: ', error);
        return utils.buildResponse(500, 'Error adding energy log');
    }
}

module.exports = {
    addEnergyLog,
    getEnergyLog
};