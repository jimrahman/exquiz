from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from itertools import count

all_queries = []
counter = count(1000)  # id generator


def Extract_received_id(path):
    if path[:10] == '/questions' and path[-22:] == '/action/selectreceiver':
        endpath = path.find('/action/selectreceiver')
        receiverid = path[11:endpath]
        if receiverid.isdigit() == True:
            return receiverid
        else:
            return "no id"
    else:
        return 'no id'


def get_answerid_extraction(path):
    if path[:8] == '/answer/' and path[8:] != '':
        answer_id = path[8:]
        if answer_id.isdigit() == True and int(answer_id) <= len(all_queries) + 999:
            return answer_id
        else:
            return "no id"
    else:
        return 'no id'


def get_questionid_extraction(path):
    if path[:11] == '/questions/' and path[11:] != '':
        question_id = path[11:]
        if question_id.isdigit() == True and int(question_id) <= len(all_queries) + 999:
            return question_id
        else:
            return 'no id'
    else:
        return 'no id'


class testHandler(BaseHTTPRequestHandler):

    def common_response(self, response=200):
        self.send_response(response)
        self.send_header('content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = self.path
        if get_questionid_extraction(path) != 'no id':
            received_id = get_questionid_extraction(path)
            url = '/questions/' + received_id
            if self.path == url:  # path created using parsed query
                for i in all_queries:
                    if i['id'] == int(received_id):  # finding matching id
                        if 'answered' in i:
                            self.common_response()
                            send_data_jsn = json.dumps(i)
                            self.wfile.write(send_data_jsn.encode())

                        else:
                            self.common_response()
                            send_data = {
                                'question': i['question'],
                                'answer': [i['answer'][0]['text'], i['answer'][1]['text'], i['answer'][2]['text']]
                            }
                            send_data_jsn = json.dumps(send_data)
                            self.wfile.write(send_data_jsn.encode())
                            print('question send')
            else:
                self.send_error(404)  # not found
        elif get_answerid_extraction(path) != 'no id':
            answer_id = get_answerid_extraction(path)
            url = '/answer/' + answer_id
            if self.path == url:
                for i in all_queries:
                    if i['id'] == int(answer_id):
                        self.common_response()
                        jsn_answer = json.dumps(i)
                        self.wfile.write(jsn_answer.encode())
            else:
                self.send_error(404)
        else:
            self.send_error(404)

    def post_data_extraction(self):
        content_length = int(self.headers['content-length'])
        request_data = self.rfile.read(content_length)
        request_data_decode = request_data.decode("utf-8")
        request_data_dict = json.loads(request_data_decode)
        return request_data_dict

    def Post_request_create_QUESTION(self):
        request_data_dict = self.post_data_extraction()

        if 'question' in request_data_dict and 'answer' in request_data_dict:
            ques_dict = {}  # question and data is added to this dict from request_data_dict
            question = request_data_dict['question']
            answer = request_data_dict['answer']
            if question == "" or answer[0]['text'] == answer[1]['text'] or answer[1]['text'] == answer[2]['text']:
                self.send_error(406)  # Not acceptable
                print('wrong information received')
            elif answer[0]['selectedBySender'] == answer[1]['selectedBySender'] and answer[1]['selectedBySender'] == \
                    answer[2]['selectedBySender']:
                self.send_error(406)  # Not acceptable
                print('wrong information received')

            else:
                id = next(counter)
                ques_dict['question'] = request_data_dict['question']  # adding ques to ques_dict
                ques_dict['answer'] = request_data_dict['answer']
                ques_dict['id'] = id  # int
                all_queries.append(ques_dict)
                self.common_response(201)
                jsn_quesid_dict = json.dumps(ques_dict['id'])
                jsn_ques_dict = json.dumps(ques_dict)
                self.wfile.write(jsn_quesid_dict.encode())
                print("data has been saved")
                print(jsn_ques_dict)
        else:
            self.send_error(406)  # Not acceptable
            print('wrong information received')

    def do_POST(self):
        path = self.path
        if path == '/questions':
            self.Post_request_create_QUESTION()
        elif Extract_received_id(path) != 'no id':
            received_id = Extract_received_id(path)
            url = '/questions/' + received_id + '/action/selectreceiver'
            if path == url and int(received_id) <= len(all_queries) + 999:
                receiver_response_dict = self.post_data_extraction()

                if 'receiverResponse' in receiver_response_dict:
                    response = {}
                    response['receiverResponse'] = receiver_response_dict['receiverResponse']
                    for i in all_queries:
                        if i['id'] == int(received_id):
                            i['answer'][0]['selectedByReceiver'] = response['receiverResponse'][0]['selectedByReceiver']
                            i['answer'][1]['selectedByReceiver'] = response['receiverResponse'][1]['selectedByReceiver']
                            i['answer'][2]['selectedByReceiver'] = response['receiverResponse'][2]['selectedByReceiver']
                            self.common_response(201)
                            if 'flag' in i:
                                self.send_error(500)
                            else:
                                result = []
                                if i['answer'][0]['selectedByReceiver'] == i['answer'][0]['selectedBySender']:
                                    result.append(1)
                                else:
                                    result.append(0)
                                if i['answer'][1]['selectedByReceiver'] == i['answer'][1]['selectedBySender']:
                                    result.append(1)
                                else:
                                    result.append(0)
                                if i['answer'][2]['selectedByReceiver'] == i['answer'][2]['selectedBySender']:
                                    result.append(1)
                                else:
                                    result.append(0)
                                send_result = json.dumps(result)
                                self.wfile.write(send_result.encode())
                                i['answered'] = 'yes'
                                print(i)







                else:
                    self.send_error(404)
        else:
            self.send_error(404)


handler = testHandler
PORT = 8989
server = HTTPServer(('', PORT), handler)
print("yes its working")
server.serve_forever()
print("server has stopped")
