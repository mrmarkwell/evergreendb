import {Injectable} from '@angular/core';
import {Http, Headers} from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { Child } from './child';

@Injectable()
export class RestService {
	constructor(private http: Http) {}

	// If we add cache to getChildren, it would reduce bandwidth.
	getChildren(): Promise<Child[]> {
		let childrenUrl = this.evergreenUrl + '/entity/fss_child';
		console.log(childrenUrl);
		return this.http.get(childrenUrl)
			.toPromise().then(response => response.json() as Child[])
			.catch(this.handleError);
	}
	getChild(id): Promise<Child> {
		return this.getChildren().then(children => children.find(child => child.id === id))
	}
	addChild(child: Child): Promise<Child> {
		let childrenUrl = this.evergreenUrl + '/entity/fss_child';
		return this.http.post(childrenUrl, JSON.stringify(child), {headers: this.headers})
			.toPromise().then(res => res.json().data as Child)
			.catch(this.handleError);
	}
	updateChild(child: Child) {
		const childUrl = this.evergreenUrl + '/entity/fss_child?id=' + child.id;
		console.log(JSON.stringify(child));
		return this.http.put(childUrl, JSON.stringify(child), {headers: this.headers})
			.toPromise().then(() => child).catch(this.handleError);
	}

	private handleError(error: any): Promise<any> {
		console.error('An error occurred', error);
		return Promise.reject(error.message || error);
	}

	private evergreenUrl = 'http://127.0.0.1:5000';
	private headers = new Headers({'Content-Type': 'application/json'});
}
