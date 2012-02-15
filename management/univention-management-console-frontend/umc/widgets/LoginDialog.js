/*
 * Copyright 2011 Univention GmbH
 *
 * http://www.univention.de/
 *
 * All rights reserved.
 *
 * The source code of this program is made available
 * under the terms of the GNU Affero General Public License version 3
 * (GNU AGPL V3) as published by the Free Software Foundation.
 *
 * Binary versions of this program provided by Univention to you as
 * well as other copyrighted, protected or trademarked materials like
 * Logos, graphics, fonts, specific documentations and configurations,
 * cryptographic keys etc. are subject to a license agreement between
 * you and Univention and not subject to the GNU AGPL V3.
 *
 * In the case you use this program under the terms of the GNU AGPL V3,
 * the program is provided in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public
 * License with the Debian GNU/Linux or Univention distribution in file
 * /usr/share/common-licenses/AGPL-3; if not, see
 * <http://www.gnu.org/licenses/>.
 */
/*global dojo dijit dojox umc console window */

dojo.provide("umc.widgets.LoginDialog");

dojo.require("umc.i18n");
dojo.require("umc.tools");
dojo.require("umc.widgets.Text");
dojo.require("umc.widgets.LabelPane");
dojo.require("umc.widgets.ComboBox");
dojo.require("umc.widgets.StandbyMixin");

dojo.declare('umc.widgets.LoginDialog', [ umc.widgets.StandbyMixin, umc.i18n.Mixin ], {
	// our own variables
	_connections: null,
	_iframe: null,
	_languageBox: null,
	_languageLabel: null,
	_text: null,

	// internal flag whether the dialog is rendered or not
	_isRendered: false,

	// use the framework wide translation file
	i18nClass: 'umc.app',

	availableLanguages: null,

	postMixInProperties: function() {
		dojo.mixin(this, {
			availableLanguages: [
				{id: 'de-DE', label: this._('German')},
				{id: 'en-US', label: this._('English')}
			]});

		this.domNode = dojo.byId('umc_LoginDialog');
	},

	defaultLang: function () {
		// dojo.locale is set in the index.html either via the query string in the URL,
		// via a cookie, or via dojo automatically
		var lowercase_locale = dojo.locale.toLowerCase();
		var exact_match = dojo.filter(this.availableLanguages, function(item) {
			return lowercase_locale == item.id.toLowerCase();
		});
		if (exact_match.length > 0) {
			return exact_match[0].id;
		}

		// fallbacks
		var default_language = null;

		// if dojo.locale is 'de' or 'de-XX' choose the first locale that starts with 'de'
		var short_locale = lowercase_locale.slice(0, 2);
		dojo.forEach(this.availableLanguages, function(lang) {
			if (lang.id.toLowerCase().indexOf(short_locale) === 0) {
				default_language = lang.id;
				return false;
			}
		}, this);

		if (null === default_language) {
			default_language = 'en-US';
		}

		console.log('new locale ' + default_language);

		return default_language;
	},

	buildRendering: function() {
		this.inherited(arguments);

		this._iframe = dojo.byId('umc_LoginDialog_Iframe');
		// initialize the iframe
		this._initForm();

		// create the upper info text
		this._text = new umc.widgets.Text({
			style: 'margin-left: auto; margin-right: auto; margin-top: 1em; width: 280px;',
			content: ''
		});
		this._text.placeAt('umc_LoginDialog', 'first');

		// create the language combobox
		var default_lang = this.defaultLang();
		this._languageBox = new umc.widgets.ComboBox({
			staticValues: this.availableLanguages,
			value: default_lang,
			sizeClass: null
		});
		this._languageLabel = new umc.widgets.LabelPane({
			label: this._('Language'),
			content: this._languageBox
		});
		// we need to manually startup the widgets
		this._languageBox.startup();
		this._languageLabel.startup();
		this._languageLabel.placeAt('umc_LoginDialog_FormContainer');
		// register onchange event
		this.connect(this._languageBox, 'onChange', function(lang) {
			if (lang != dojo.locale) {
				// reload the page when a different language is selected
				var query = dojo.queryToObject(window.location.search.substring(1));
				query.lang = lang;
				dojo.cookie('UMCLang', query.lang, { expires: 100, path: '/' });
				window.location.search = '?' + dojo.objectToQuery(query);
			}
		});
	},

	_initForm: function() {
		// wait until the iframe is completely loaded
		setTimeout(dojo.hitch(this, function() {
			// check whether the form is available or not
			var	isLoaded = dojo.getObject('contentWindow.ready', false, this._iframe);
			if (!isLoaded) {
				// we can't access the form, therefore we need to trigger the
				// function again
				this._initForm();
			} else {
				// we are able to access the form
				dojo.withGlobal(this._iframe.contentWindow, dojo.hitch(this, function() {
					// because of the iframe we need to manually translate the content
					dojo.attr(dojo.byId('umc_LabelPane_Username'), 'innerHTML', this._('Username'));
					dojo.attr(dojo.byId('umc_LabelPane_Password'), 'innerHTML', this._('Password'));
					dojo.attr(dojo.byId('umc_SubmitButton_label'), 'innerHTML', this._('Login'));
				}));

				// each time the page is loaded, we need to connect to the form events
				this._connectEvents();

				this._isRendered = true;
			}
		}), 500);
	},

	_connectEvents: function() {
		// TODO: cleanup?
		var form;
		var usernameInput;
		var usernameContainer;
		var passwordInput;
		var passwordContainer;

		dojo.withGlobal(this._iframe.contentWindow, dojo.hitch(this, function() {
			form = dojo.byId('umc_Form');
			usernameInput = dojo.byId('umc_UsernameInput');
			usernameContainer = dojo.byId('umc_UsernameContainer');
			passwordInput = dojo.byId('umc_PasswordInput');
			passwordContainer = dojo.byId('umc_PasswordContainer');
		}));

		this._connections = [];
		// register all events
		this._connections.push(
			this.connect(form, 'onsubmit', function(event) {
				this._authenticate(usernameInput.value, passwordInput.value);
				this._isRendered = false;
				this._initForm();
			})
		);

		var fields = [
			[usernameInput, usernameContainer],
			[passwordInput, passwordContainer]
		];
		var settingsArray = [
			['onmouseover', this._setHover, true],
			['onmouseout', this._setHover, false],
			['onfocus', this._setFocus, true],
			['onblur', this._setFocus, false]
		];
		dojo.forEach(fields, dojo.hitch(this, function(field) {
			var input = field[0];
			var container = field[1];
			dojo.forEach(settingsArray, dojo.hitch(this, function(setting) {
				var event = setting[0];
				var func = setting[1];
				var flag = setting[2];
				this._connections.push(
					dojo.connect(input, event, function(e) {
						func(container, flag);
					})
				);
			}));
		}));
	},

	_disconnectEvents: function() {
		dojo.forEach(this._connections, dojo.disconnect);
	},

	_setInitialFocus: function() {
		dojo.withGlobal(this._iframe.contentWindow, dojo.hitch(this, function() {
			// initial focus on username input
			dojo.byId('umc_UsernameInput').focus();
			this._setFocus(dojo.byId('umc_UsernameContainer'), true);
		}));
	},

	_setFocus: function(obj, enable) {
		if (enable === true) {
			dojo.addClass(obj, 'dijitTextBoxFocused dijitValidationTextBoxFocused dijitFocused');
		} else if (enable === false) {
			dojo.removeClass(obj, 'dijitTextBoxFocused dijitValidationTextBoxFocused dijitFocused');
		}
	},

	_setHover: function(obj, enable) {
		if (enable === true) {
			dojo.addClass(obj, 'dijitTextBoxHover dijitValidationTextBoxHover dijitHover');
		} else if (enable === false) {
			dojo.removeClass(obj, 'dijitTextBoxHover dijitValidationTextBoxHover dijitHover');
		}
	},

	_authenticate: function(username, password) {
		this.standby(true);
		umc.tools.umcpCommand('auth', {
			username: username,
			password: password
		}).then(dojo.hitch(this, function(data) {
			// disable standby in any case
			this.standby(false);

			// make sure that we got data
			this.onLogin(username);
			this.hide();
		}), dojo.hitch(this, function(error) {
			// disable standby in any case
			this.standby(false);
		}));
	},

	show: function() {
		// update info text
		var msg = '';
		if (umc.tools.status('setupGui')) {
			// user has already logged in before, show message for relogin
			msg = '<p>' + this._('Your session has been closed due to inactivity. Please login again.') + '</p>';
		} else {
			msg = '<p>' + this._('Welcome to Univention Management Console. Please enter your domain username and password for login.') + '</p>';

			// Show warning if connection is unsecured
			if (window.location.protocol === 'http:') {
				msg += '<p style="margin: 5px 0;"><b>' + this._('Insecure Connection') + ': </b>';
				msg += this._('This network connection is not encrypted. All personal or sensitive data will be transmitted in plain text. Please follow %s this link</a> to use a secure SSL connection.', '<a href="https://' + window.location.href.slice(7) + '">') + '</p>';
			}
		}

		// if login failed display a notification
		msg += '<p class="umc_LoginMessage" style="display: none; color: #ff0000;"></p>';

		this._text.set('content', msg);

		if (this._isRendered) {
			dojo.query('.umcShowHide').style('display', 'block');
			this._setInitialFocus();
		} else {
			var handler = this.connect(this, '_connectEvents', function() {
				dojo.query('.umcShowHide').style('display', 'block');
				this._setInitialFocus();
				this.disconnect(handler);
			});
		}
	},

	hide: function() {
		// hide the dialog
		dojo.query('.umcShowHide').style('display', 'none');
	},

	onLogin: function(/*String*/ username) {
		// event stub
	}
});
