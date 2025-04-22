#!/usr/bin/env python

"""
  Apache VirtualHost Creation

  RCS-ID:      $Id: isoloader.py, v0.1 20.08.2019 18:28 Worked Exp $
  Author:      Worked <operador@gmail.com>
  Created:     20.08.2019 v0.1 isoloader.py
  License:     GNU General Public License v3.0 

  That Python file is free software; you can redistribute it and/or modify it
  under the terms of the GNU General Public License as published by the Free
  Software Foundation; either version 2 of the License, or (at your option)
  any later version.

  That Python file is distributed in the hope that it will be, useful but
  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
  for more details.

  You should have received a copy of the GNU General Public License
  along with Windows Live Messenger Class; if not, write to the Free Software
  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import argparse
import os

class virtualhost:
    """
    Creacion de archivos virtualhost rapida y sencilla para que todos tengan
    los mismos patrones y no nos volvamos locos.
    """
    def __init__(self, mode, host, mail, proxy):
        # Variables de uso interno
        self.mode = mode.lower()
        self.host = host.lower()
        self.mail = mail.lower()
        self.proxy = proxy

    def __repr__(self):
        #print 'a2newsite: iniciando nuevo VirtualHost %s (modo: %s).' % (self.host, self.mode)
        try:
            with open('/etc/apache2/sites-available/%s.conf' % self.host, 'w') as final, open('/root/.apache2/%s.conf' % self.mode, 'r') as demo:
                virtual = demo.read()
                # Reemplazamos las variables segun el caso...
                if self.mode == 'default':
                    virtual = virtual % (self.host, self.mail, self.host, self.host, self.host, self.host)
                elif self.mode == 'both':
                    virtual = virtual % (self.host, self.mail, self.host, self.host, self.host, self.host, self.host, self.mail, self.host, self.host, self.host, self.host, self.host)
                elif self.mode == 'ssl':
                    virtual = virtual % (self.host, self.mail, self.host, self.host, self.host, self.mail, self.host, self.host, self.host, self.host, self.host)

                # Escribimos el archivo final
                final.write(virtual)

                # Creamos la ruta en /var/www...
                if not os.path.exists('/var/www/%s' % self.host):
                    os.makedirs('/var/www/%s' % self.host)

                # Ale, todo como dios manda ya
                return 'a2newsite: VirtualHost %s establecido correctamente.' % (self.host)
        except IOError as e:
            return "a2newsite: ({0}) - {1}".format(e.errno, e.strerror)
            exit(1)
# - --  ---   ------------------------------------------------------------

""" Command line parser
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog='a2newsite',
            description='Configura dominios de una forma sencilla...',
            epilog='always use a2newsite, make your day on internet more safely')

    # Comandos aceptados
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-normal', action='store_true', help='crea un virtualhost sin SSL.')
    group.add_argument('-both', action='store_true', help='crea un virtualhost sin y con SSL.')
    group.add_argument('-ssl', action='store_true', help='crea un virtualhost con SSL.')

    parser.add_argument('-proxy', action='store_true', help='activa la opcion de proxy.')
    parser.add_argument('-email', metavar='mail', default="dummie@localhost.org", help='cambia el email de contacto (defecto: dummie@localhost.org).')
    parser.add_argument('-sitio', metavar='site', help='nombre del sitio web.')

    parser.add_argument('-version', action='version', version='%(prog)s 1.0')

    # Iniciamos el parser
    args = parser.parse_args()

    # Debugueo del bueno y rico
    #print args

    # Magia que comienza aqui....
    if args.normal:
        print virtualhost('default', args.sitio, args.email, args.proxy)
    elif args.both:
        print virtualhost('both', args.sitio, args.email, args.proxy)
    elif args.ssl:
        print virtualhost('ssl', args.sitio, args.email, args.proxy)
