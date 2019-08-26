class SVGManifest
	# filename
	# server socket_address
	constructor: (options)->
		if not "WebSocket" in window
			if alertify
					alertify.error "Websockets not supported"
			return
		this.ws = new WebSocket(options.socket_address)
		this.ws.onopen = (e)->
			if alertify
				alertify.notify "SVGManifest opened"
			return
		this.ws.onmessage = (e)->
			try
				msg = JSON.parse(e.data)
				console.log "WS", msg
			catch
				if alertify
					alertify.error "Malformed message"
		this.ws.onclose = (e)->
			if alertify
				alertify.notify "SVGManifest closed"
		this.ws.onerror = (e)->
			if alertify
				alertify.notify "SVGManifest Error", e.data
