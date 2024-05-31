from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__)


@app.route('/download', methods=['POST', 'GET'])
def download_file():
    folder_path = 'from_python310'  # 替换成你想要下载文件的文件夹路径
    filename = request.args.get('filename')
    print(filename)

    if not os.path.isfile(os.path.join(folder_path ,filename)):
        return jsonify({'error': 'File not found'}), 404

    return send_from_directory(folder_path, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='::', port=8000, debug=True)
