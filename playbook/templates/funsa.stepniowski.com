server {
	server_name {{ domain }};

	access_log {{ webapps_dir }}/{{ app_name }}/log/nginx-access.log;
	error_log {{ webapps_dir }}/{{ app_name }}/log/nginx-error.log;

	root {{ webapps_dir }}/{{ app_name }}/src;
	index index.html index.htm;

	location / {
  	      include uwsgi_params;
	      uwsgi_pass unix:/tmp/{{ app_name }}.sock;
	}
}
