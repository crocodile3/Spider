# Spider
爬虫基础知识点总结

## 1.安装requests库
<pre><code>pip install requests</code></pre>

## 2.requests常见的功能用法
### 2.1.1发送请求-requests.get(url)
<pre><code>r = requests.get('https://www.baidu.com/') </code></pre>
### 2.1.2其他请求方式
<pre><code>r = requests.put("http://httpbin.org/put")
r = requests.delete("http://httpbin.org/delete")
r = requests.head("http://httpbin.org/get")
r = requests.options("http://httpbin.org/get")</code></pre>

### 2.2传递参数-requestr(url,params)
Requests 允许你使用 params 关键字参数，以一个字符串字典来提供这些参数
<pre><code>>>> payload = {'key1': 'value1', 'key2': 'value2'}
>>> r = requests.get("http://httpbin.org/get", params=payload)</code></pre>

### 2.3响应内容-r.text
<pre><code>>>> r = requests.get('https://github.com/timeline.json')
>>> r.text</code></pre>

### 2.4二进制响应内容-r.content
<pre><code>
>>> r.content
b'[{"repository":{"open_issues":0,"url":"https://github.com/...
</code></pre>

### 2.5JSON响应内容-r.json
<pre><code>
>>> r = requests.get('https://github.com/timeline.json')
>>> r.json()
</code></pre>
注：JSON解析失败会报异常：ValueError: No JSON object could be decoded；
响应失败也可能会将错误信息以JSON格式的返回，这时就需要使用r.raise_for_status() 或者检查 r.status_code是否和你的期望相同

2.6原始响应内容：r.raw
注意需要在请求中加stream=True:requests.get(url,stream=True)
<pre><code>
>>> r = requests.get('https://github.com/timeline.json', stream=True)
>>> r.raw
<requests.packages.urllib3.response.HTTPResponse object at 0x101194810>
>>> r.raw.read(10)
'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03'
</code></pre>

## 3请求头处理
### 3.1给http添加请求头：传递一个 dict 给 headers 参数
<pre><code>
>>> url = 'https://api.github.com/some/endpoint'
>>> headers = {'user-agent': 'my-app/0.0.1'}
>>> r = requests.get(url, headers=headers)
</code></pre>

### 3.2给post请求增加数据
<pre><code>
>>> payload = {'key1': 'value1', 'key2': 'value2'}
>>> r = requests.post("http://httpbin.org/post", data=payload)
>>> print(r.text)
{
  ...
  "form": {
    "key2": "value2",
    "key1": "value1"
  },
  ...
}
</code></pre>
注：当多个元素使用同一key的时候，可以采用元组传递参数

### 3.3获取响应状态码
<pre><code>
>>> r = requests.get('http://httpbin.org/get')
>>> r.status_code
</code></pre>
如果请求发生异常，则可以通过Response.raise_for_status()来抛出异常，当请求正常时，获取的status_code 是 200 ，则Response.raise_for_status()的返回值为None
<pre><code>
>>> r.raise_for_status()
None
</code></pre>

## 4.响应头-r.headers
<pre><code>
>>> r.headers
{
    'content-encoding': 'gzip',
    'transfer-encoding': 'chunked',
    'connection': 'close',
    'server': 'nginx/1.0.4',
    'x-runtime': '148ms',
    'etag': '"e1ca502697e5c9317743dc078f67693f"',
    'content-type': 'application/json'
}
</code></pre>

## 5.Cookie
- 访问响应中的Cookie值
<pre><code>
>>> url = 'http://example.com/some/cookie/setting/url'
>>> r = requests.get(url)
>>> r.cookies['example_cookie_name']
</code></pre>
- 在请求中加Cookie信息
<pre><code>
>>> url = 'http://httpbin.org/cookies'
>>> cookies = dict(cookies_are='working')
>>> r = requests.get(url, cookies=cookies)
</code></pre>

## 6.设置超时
<pre><code>
>>> requests.get('http://github.com', timeout=0.001)
</code></pre>
注：timeout 仅对连接过程有效，与响应体的下载无关。 timeout 并不是整个下载响应的时间限制，而是如果服务器在 timeout 秒内没有应答，将会引发一个异常（更精确地说，是在 timeout 秒内没有从基础套接字上接收到任何字节的数据时）If no timeout is specified explicitly, requests do not time out.

## 7.常见错误与异常
- 遇到网络问题（如：DNS 查询失败、拒绝连接等）时，Requests 会抛出一个 **ConnectionError** 异常

- 如果 HTTP 请求返回了不成功的状态码， Response.raise_for_status() 会抛出一个 **HTTPError** 异常

- 若请求超时，则抛出一个 **Timeout** 异常

- 若请求超过了设定的最大重定向次数，则会抛出一个 **TooManyRedirects** 异常

- 所有Requests显式抛出的异常都继承自 **requests.exceptions.RequestException** 
