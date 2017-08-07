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

	private handleError(error: any): Promise<any> {
		console.error('An error occurred', error);
		return Promise.reject(error.message || error);
	}

	private evergreenUrl = 'http://127.0.0.1:5000';
	private headers = new Headers({'Content-Type': 'application/json'});
}
