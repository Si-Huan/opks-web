import csv
from flask import Flask, request
from opks import dfm, kzd, sbd
from werkzeug.wrappers import Response
from io import StringIO
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/gei_ye_suan", methods=['POST'])
def suan():
    all_od = request.get_data().decode("utf-8").splitlines()
    resp = {'data': []}
    for line in all_od:
        if line[0] == '`':
            continue
        od = line.split()
        if line[0] == '#':
            now_kzd = kzd(od[0], float(od[1]), float(
                od[2]), float(od[3]), float(od[4]))
        else:
            hdfm = dfm(int(od[4]), int(od[5]), int(od[6]))
            # vdfm = dfm(int(od[6]), int(od[7]), int(od[9]))
            vdfm = dfm(90, 0, 0)
            now_sbd = sbd(od[0], float(od[1]), float(od[2]),
                          float(od[3]), hdfm, vdfm, now_kzd)
            resp['data'].append(now_sbd.for_web_print())
    return resp


@app.route("/gei_ye_cass", methods=['POST'])
def cass():
    all_od = request.get_data().decode("utf-8").splitlines()

    def generate():
        data = StringIO()
        w = csv.writer(data)
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)
        # write
        for line in all_od:
            if line[0] == '`':
                continue
            od = line.split()
            if line[0] == '#':
                now_kzd = kzd(od[0], float(od[1]), float(
                    od[2]), float(od[3]), float(od[4]))
            else:
                hdfm = dfm(int(od[4]), int(od[5]), int(od[6]))
                # vdfm = dfm(int(od[6]), int(od[7]), int(od[9]))
                vdfm = dfm(90, 0, 0)
                now_sbd = sbd(od[0], float(od[1]), float(od[2]),
                              float(od[3]), hdfm, vdfm, now_kzd)
                w.writerow(now_sbd.for_cass())
                yield data.getvalue()
                data.seek(0)
                data.truncate(0)

    # stream the response as the data is generated
    response = Response(generate(), mimetype='text/csv')
    # add a filename
    response.headers.set("Content-Disposition",
                         "attachment", filename="cass.dat")
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7171)
