# Install Nginx
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
file { '/data/':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  recurse => true,
}

file { '/data/web_static/':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases/':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/shared/':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases/test/':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => 'Test Page',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create or recreate the symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  force  => true,
}

# Update Nginx configuration
file_line { 'nginx_config':
  path    => '/etc/nginx/sites-available/default',
  line    => 'location /hbnb_static/ {',
  match   => 'listen 80 default_server;',
  after   => 'listen 80 default_server;',
  notify  => Service['nginx'],
  require => Package['nginx'],
}

file_line { 'nginx_config_alias':
  path    => '/etc/nginx/sites-available/default',
  line    => "\t\talias /data/web_static/current/;",
  match   => 'location /hbnb_static/ {',
  after   => 'location /hbnb_static/ {',
  notify  => Service['nginx'],
  require => Package['nginx'],
}

# Restart Nginx
service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => [File['/etc/nginx/sites-available/default'], File['/data/web_static/current']],
}
