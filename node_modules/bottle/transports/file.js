var fs = require('fs')
  , tide = require('tide');

module.exports = function(path, flag) {
  function log(logger, time, level, message) {
    var timestamp = tide.utc('YYYY-MM-DD hh:mm:ss.mmms UTC', time);
    log.stream.write(timestamp + ' # ' + level + ': ' + message + '\n');
  }

  log.stream = fs.createWriteStream(path, { flags: flag || 'a' });
  return log;
};
