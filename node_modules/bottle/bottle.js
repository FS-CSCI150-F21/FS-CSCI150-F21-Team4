var util = require('util')
  , EventEmitter = require('events').EventEmitter
  , nothing = function() {};


// `Array.prototype.slice` shorthand
function __slice(subject, offset) {
  return Array.prototype.slice.call(subject, offset || 0);
}


// a logger instance
function Logger(levels) {
  var self = this;

  EventEmitter.call(this);

  // suppress exceptions caused by an "error" event without any listeners
  this.on('error', nothing);

  this._transports = [];
  this._levels = levels;

  // add a method for each logging level
  for (var i = 0; i < levels.length; i++) {
    (function(level){
      self[level] = function() {
        self._log.apply(self, [level].concat(__slice(arguments)));
      };
    })(levels[i]);
  }
}

util.inherits(Logger, EventEmitter);


// fans a log event out to all transports
Logger.prototype._log = function(level) {
  var i, transport
    , time = new Date()
    , args = __slice(arguments, 1)
    , message = this._format.apply(this, args);

  for (i = 0; i < this._transports.length; i++) {
    transport = this._transports[i];
    if (transport.levels.indexOf(level) !== -1) {
      transport.fn(this, time, level, message, args);
    }
  }

  this.emit(level, time, message, args);
};


// essentially like `util.format`, but with the added "%v" token
Logger.prototype._format = function(format) {
  var args = __slice(arguments, 1)
    , i = 0;

  return format.replace(/%[%sdjv]/g, function(match) {
    if (match === '%%' || i === args.length) {
      return match;
    }

    switch (match) {
      case '%j': return JSON.stringify(args[i++]);
      case '%v': return util.inspect(args[i++]).replace(/\s*\n\s+/g, ' ');
      case '%s': return '' + args[i++];
      case '%d': return +args[i++];
    }
  });
};


// attaches a transport to the logger
Logger.prototype.add = function(transport, options) {
  var from, to
    , levels = this._levels;

  if (typeof options === 'object' && options != null) {
    if (Array.isArray(options)) {
      levels = options;
    } else {
      if ((from = levels.indexOf(options.from)) === -1) { from = 0; }
      if ((levels.indexOf(options.to) + 1) === 0) { to = levels.length; }

      levels = levels.slice(from, to);
    }
  }

  this._transports.push({ levels: levels, fn: transport });
};


// instantiates a new logger instance
exports.create = function(levels) {
  return new Logger(levels);
};


// bundled transports
exports.file = require('./transports/file.js');
exports.plain = require('./transports/plain.js');
