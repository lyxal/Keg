// Transcrypt'ed from Python, 2018-11-08 14:52:41
var For = {};
var If = {};
var While = {};
var random = {};
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as __module_For__ from './For.js';
__nest__ (For, '', __module_For__);
import * as __module_If__ from './If.js';
__nest__ (If, '', __module_If__);
import * as __module_While__ from './While.js';
__nest__ (While, '', __module_While__);
import * as __module_random__ from './random.js';
__nest__ (random, '', __module_random__);
var __name__ = '__main__';
export var LENGTH = '!';
export var DUPLICATE = ':';
export var POP = '_';
export var _print_CHR = ',';
export var _print_INT = '.';
export var INPUT = '?';
export var L_SHIFT = "'";
export var R_SHIFT = '"';
export var RANDOM = '~';
export var REVERSE = '^';
export var SWAP = '$';
export var COMMENT = '#';
export var BRANCH = '|';
export var ESCAPE = '\\';
export var C_STRING = '`';
export var REGISTER = '&';
export var FUNCTION = '@';
export var MATHS = '+-*/%';
export var CONDITIONAL = '<>=';
export var NUMBERS = '0123456789';
export var TAB = '\t';
export var ALT_TAB = '    ';
export var NEWLINE = '\n';
export var START = 'start';
export var END = 'end';
export var BODY = 'body';
export var FOR_LOOP = dict ([[START, '('], [END, ')']]);
export var IF_STMT = dict ([[START, '['], [END, ']']]);
export var WHILE_LOOP = dict ([[START, '{'], [END, '}']]);
export var stack = list ([]);
export var register = null;
export var comment = false;
export var escape = false;
export var _printed = false;
export var _eval = function (expression) {
	var temp = list ([]);
	for (var char of expression) {
		if (__in__ (char, NUMBERS)) {
			temp.append (int (char));
		}
		else if (__in__ (char, MATHS)) {
			var __left0__ = tuple ([temp.py_pop (), temp.py_pop ()]);
			var x = __left0__ [0];
			var y = __left0__ [1];
			temp.append (eval ('y{0}x'.format (char)));
		}
		else if (__in__ (char, CONDITIONAL)) {
			var __left0__ = tuple ([temp.py_pop (), temp.py_pop ()]);
			var lhs = __left0__ [0];
			var rhs = __left0__ [1];
			if (char == '=') {
				var char = '==';
			}
			var result = eval ('lhs{0}rhs'.format (char));
			if (result) {
				temp.append (1);
			}
			else {
				temp.append (0);
			}
		}
		else if (char == LENGTH) {
			temp.append (len (stack));
		}
		else if (char == DUPLICATE) {
			temp.append (stack [-(1)]);
		}
		else if (char == RANDOM) {
			temp.append (random.randint (0, 32767));
		}
		else if (char == POP) {
			temp.append (stack.py_pop ());
		}
		else if (char == NEWLINE || char == TAB) {
			continue;
		}
		else if (__in__ (char, '#|`@')) {
			var __except0__ = SyntaxError ('Invalid symbol in expression: ' + expression);
			__except0__.__cause__ = null;
			throw __except0__;
		}
		else {
			temp.append (ord (char));
		}
	}
	return temp [0];
};
export var py_split = function (source) {
	var source = list (source.py_replace (TAB, ''));
	var structures = dict ({'If': 0, 'While': 0, 'For': 0});
	var indexes = list ([]);
	var index = dict ([[START, 0], [END, 0], [BODY, null]]);
	var structure = null;
	for (var i = 0; i < len (source); i++) {
		var char = source [i];
		if (__in__ (char, FOR_LOOP.py_values ())) {
			if (char == FOR_LOOP [START]) {
				if (max (structures.py_values ()) == 0) {
					var structure = 'For';
					index [START] = i;
				}
				structures ['For']++;
			}
			else {
				if (list (structures.py_values ()).count (0) == 2) {
					if (structures ['For'] == 1 && structure == 'For') {
						index [END] = i;
						index [BODY] = For.extract (''.join (source.__getslice__ (index [START], index [END] + 1, 1)));
						indexes.append (index);
						var index = dict ([[START, 0], [END, 0], [BODY, null]]);
						var structure = null;
					}
				}
				structures ['For']--;
			}
		}
		else if (__in__ (char, WHILE_LOOP.py_values ())) {
			if (char == WHILE_LOOP [START]) {
				if (max (structures.py_values ()) == 0) {
					var structure = 'While';
					index [START] = i;
				}
				structures ['While']++;
			}
			else {
				if (list (structures.py_values ()).count (0) == 2) {
					if (structures ['While'] == 1 && structure == 'While') {
						index [END] = i;
						index [BODY] = While.extract (''.join (source.__getslice__ (index [START], index [END] + 1, 1)));
						indexes.append (index);
						var index = dict ([[START, 0], [END, 0], [BODY, null]]);
						var structure = null;
					}
				}
				structures ['While']--;
			}
		}
		else if (__in__ (char, IF_STMT.py_values ())) {
			if (char == IF_STMT [START]) {
				if (max (structures.py_values ()) == 0) {
					var structure = 'If';
					index [START] = i;
				}
				structures ['If']++;
			}
			else {
				if (list (structures.py_values ()).count (0) == 2) {
					if (structures ['If'] == 1 && structure == 'If') {
						index [END] = i;
						index [BODY] = If.extract (''.join (source.__getslice__ (index [START], index [END] + 1, 1)));
						indexes.append (index);
						var index = dict ([[START, 0], [END, 0], [BODY, null]]);
						var structure = null;
					}
				}
				structures ['If']--;
			}
		}
		else if (structure === null) {
			index [START] = i;
			index [END] = i;
			index [BODY] = source [i];
			indexes.append (index);
			var index = dict ([[START, 0], [END, 0], [BODY, null]]);
		}
	}
	var py_new = list ([]);
	for (var index of indexes) {
		py_new.append (index [BODY]);
	}
	return py_new;
};
export var run = function (source) {
	if (py_typeof (source) == str) {
		var code = py_split (source);
	}
	else if (py_typeof (source) != list) {
		var __except0__ = py_TypeError ('The given code is not of a supported type');
		__except0__.__cause__ = null;
		throw __except0__;
	}
	else {
		var code = source;
	}
	for (var cmd of code) {
		if (comment) {
			if (cmd == NEWLINE) {
				comment = false;
			}
			continue;
		}
		if (escape) {
			escape = false;
			stack.append (ord (cmd));
			continue;
		}
		if (cmd == LENGTH) {
			stack.append (len (stack));
		}
		else if (cmd == DUPLICATE) {
			stack.append (stack [-(1)]);
		}
		else if (cmd == POP) {
			stack.py_pop ();
		}
		else if (cmd == _print_CHR) {
			_print (chr (stack.py_pop ()), __kwargtrans__ ({end: ''}));
			_printed = true;
		}
		else if (cmd == _print_INT) {
			_print (stack.py_pop (), __kwargtrans__ ({end: ''}));
			_printed = true;
		}
		else if (cmd == L_SHIFT) {
			stack.append (stack [0]);
			delete stack [0];
		}
		else if (cmd == R_SHIFT) {
			stack.insert (0, stack.py_pop ());
		}
		else if (cmd == RANDOM) {
			stack.append (random.randint (0, 32767));
		}
		else if (cmd == REVERSE) {
			stack.reverse ();
		}
		else if (cmd == SWAP) {
			var __left0__ = tuple ([stack [-(2)], stack [-(1)]]);
			stack [-(1)] = __left0__ [0];
			stack [-(2)] = __left0__ [1];
		}
		else if (cmd == INPUT) {
			var x = alert ();
			stack.append (-(1));
			for (var char of py_reversed (x)) {
				stack.append (ord (char));
			}
		}
		else if (cmd == COMMENT) {
			comment = true;
		}
		else if (cmd == BRANCH) {
			continue;
		}
		else if (cmd == ESCAPE) {
			escape = true;
		}
		else if (cmd == REGISTER) {
			if (register === null) {
				register = stack.py_pop ();
			}
			else {
				stack.append (register);
				register = null;
			}
		}
		else if (py_typeof (cmd) == dict) {
			if (__in__ (1, cmd)) {
				var test = stack.py_pop ();
				if (test) {
					run (cmd [1]);
				}
				else {
					run (cmd [0]);
				}
			}
			else if (__in__ ('count', cmd)) {
				var n = _eval (cmd ['count']);
				for (var q = 0; q < n; q++) {
					run (cmd ['body']);
				}
			}
			else if (__in__ ('condition', cmd)) {
				var condition = cmd ['condition'];
				while (_eval (condition)) {
					run (cmd ['body']);
				}
			}
			else {
				var __except0__ = Exception ('Oh, uh, could you get me the milk!');
				__except0__.__cause__ = null;
				throw __except0__;
			}
		}
		else if (__in__ (cmd, MATHS)) {
			var __left0__ = tuple ([stack.py_pop (), stack.py_pop ()]);
			var x = __left0__ [0];
			var y = __left0__ [1];
			stack.append (eval ('y{0}x'.format (cmd)));
		}
		else if (__in__ (cmd, CONDITIONAL)) {
			var __left0__ = tuple ([stack.py_pop (), stack.py_pop ()]);
			var lhs = __left0__ [0];
			var rhs = __left0__ [1];
			if (cmd == '=') {
				var cmd = '==';
			}
			var result = eval ('rhs{0}lhs'.format (cmd));
			if (result) {
				stack.append (1);
			}
			else {
				stack.append (0);
			}
		}
		else if (__in__ (cmd, NUMBERS)) {
			stack.append (int (cmd));
		}
		else if (cmd == TAB) {
			continue;
		}
		else if (cmd == ALT_TAB) {
			continue;
		}
		else if (cmd == NEWLINE) {
			continue;
		}
		else {
			stack.append (ord (cmd));
		}
	}
};
export var _print = function () {
	for (var arg of args) {
		document.getElementById ('output').innerHTML += arg;
	}
};
if (__name__ == '__main__') {
	var code = document.getElementById ('codebox').innerHTML;
	run (code);
	if (!(_printed)) {
		var _printing = '';
		for (var item of stack) {
			if (item < 10 || item > 256) {
				_printing += str (item) + ' ';
			}
			else {
				_printing += chr (item);
			}
		}
		__print (_printing);
	}
}

//# sourceMappingURL=index.map