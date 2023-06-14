'''
100 	Continue 	[RFC9110, Section 15.2.1]
101 	Switching Protocols 	[RFC9110, Section 15.2.2]
102 	Processing 	[RFC2518]
103 	Early Hints 	[RFC8297]
104-199 	Unassigned
200 	OK 	[RFC9110, Section 15.3.1]
201 	Created 	[RFC9110, Section 15.3.2]
202 	Accepted 	[RFC9110, Section 15.3.3]
203 	Non-Authoritative Information 	[RFC9110, Section 15.3.4]
204 	No Content 	[RFC9110, Section 15.3.5]
205 	Reset Content 	[RFC9110, Section 15.3.6]
206 	Partial Content 	[RFC9110, Section 15.3.7]
207 	Multi-Status 	[RFC4918]
208 	Already Reported 	[RFC5842]
209-225 	Unassigned
226 	IM Used 	[RFC3229]
227-299 	Unassigned
300 	Multiple Choices 	[RFC9110, Section 15.4.1]
301 	Moved Permanently 	[RFC9110, Section 15.4.2]
302 	Found 	[RFC9110, Section 15.4.3]
303 	See Other 	[RFC9110, Section 15.4.4]
304 	Not Modified 	[RFC9110, Section 15.4.5]
305 	Use Proxy 	[RFC9110, Section 15.4.6]
306 	(Unused) 	[RFC9110, Section 15.4.7]
307 	Temporary Redirect 	[RFC9110, Section 15.4.8]
308 	Permanent Redirect 	[RFC9110, Section 15.4.9]
309-399 	Unassigned
400 	Bad Request 	[RFC9110, Section 15.5.1]
401 	Unauthorized 	[RFC9110, Section 15.5.2]
402 	Payment Required 	[RFC9110, Section 15.5.3]
403 	Forbidden 	[RFC9110, Section 15.5.4]
404 	Not Found 	[RFC9110, Section 15.5.5]
405 	Method Not Allowed 	[RFC9110, Section 15.5.6]
406 	Not Acceptable 	[RFC9110, Section 15.5.7]
407 	Proxy Authentication Required 	[RFC9110, Section 15.5.8]
408 	Request Timeout 	[RFC9110, Section 15.5.9]
409 	Conflict 	[RFC9110, Section 15.5.10]
410 	Gone 	[RFC9110, Section 15.5.11]
411 	Length Required 	[RFC9110, Section 15.5.12]
412 	Precondition Failed 	[RFC9110, Section 15.5.13]
413 	Content Too Large 	[RFC9110, Section 15.5.14]
414 	URI Too Long 	[RFC9110, Section 15.5.15]
415 	Unsupported Media Type 	[RFC9110, Section 15.5.16]
416 	Range Not Satisfiable 	[RFC9110, Section 15.5.17]
417 	Expectation Failed 	[RFC9110, Section 15.5.18]
418 	(Unused) 	[RFC9110, Section 15.5.19]
419-420 	Unassigned
421 	Misdirected Request 	[RFC9110, Section 15.5.20]
422 	Unprocessable Content 	[RFC9110, Section 15.5.21]
423 	Locked 	[RFC4918]
424 	Failed Dependency 	[RFC4918]
425 	Too Early 	[RFC8470]
426 	Upgrade Required 	[RFC9110, Section 15.5.22]
427 	Unassigned
428 	Precondition Required 	[RFC6585]
429 	Too Many Requests 	[RFC6585]
430 	Unassigned
431 	Request Header Fields Too Large 	[RFC6585]
432-450 	Unassigned
451 	Unavailable For Legal Reasons 	[RFC7725]
452-499 	Unassigned
500 	Internal Server Error 	[RFC9110, Section 15.6.1]
501 	Not Implemented 	[RFC9110, Section 15.6.2]
502 	Bad Gateway 	[RFC9110, Section 15.6.3]
503 	Service Unavailable 	[RFC9110, Section 15.6.4]
504 	Gateway Timeout 	[RFC9110, Section 15.6.5]
505 	HTTP Version Not Supported 	[RFC9110, Section 15.6.6]
506 	Variant Also Negotiates 	[RFC2295]
507 	Insufficient Storage 	[RFC4918]
508 	Loop Detected 	[RFC5842]
509 	Unassigned
510 	Not Extended (OBSOLETED) 	[RFC2774][status-change-http-experiments-to-historic]
511 	Network Authentication Required 	[RFC6585]
512-599 	Unassigned
'''

from enum import Enum



INTENT_MATRIX_FILE_DSNT_EXIST_ERROR = {"code": 512, "message": "Intent matrix file not found"}
INTENT_MATRIX_FILE_STRUCTURE_ERROR = {"code": 513, "message": "Cannot parse intent matrix file normally"}
INTENT_MATRIX_FILE_PATH_IS_NONE =  {"code": 514, "message": "Intent matrix file path was not determined"}

INTENT_MATRIX_WEIGHTS_FILE_DSNT_EXIST_ERROR = {"code": 515, "message": "Intent matrix weights file not found"}
INTENT_MATRIX_WEIGHTS_FILE_STRUCTURE_ERROR = {"code": 516, "message": "Cannot parse intent weights matrix file normally"}
INTENT_MATRIX_WEIGHTS_FILE_PATH_IS_NONE =  {"code": 517, "message": "Intent matrix weights file path was not determined"}


EACH_CONVERSATION_LEN_IS_ZERO = {"code": 518, "message": "Each conversation len in zero"}
ONLY_BOT_IS_IN_CONVERSATION = {"code": 519, "message": "It is bots monolog"}
ONLY_HUMAN_IS_IN_CONVERSATION = {"code": 520, "message": "It is human monolog"}

