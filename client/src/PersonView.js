
import axios from 'axios';
import React from 'react';
import {
	Link,
} from 'react-router-dom';
import Button from '@material-ui/core/Button';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import { HOST_ADDR } from './consts';

class PersonView extends React.Component {

	constructor(props) {
		super(props);
		this.state = {personId: props.personId, person: {}};
		this.cancelTokens = [];
	}

	buildElements = (o) => {
		if (typeof(o) === 'object') {
			let out = [];
			let key = 1;
			for (let i in o) {
				let v = o[i];
				out.push(<div key={key++}>{v}</div>);
			}
			return out;
		} else {
			return o;
		}
	};

	buildRow = (name, value) => {
		return value ? (
			<TableRow>
				<TableCell>{name}</TableCell>
				<TableCell>{this.buildElements(value)}</TableCell>
			</TableRow>
		) : null;
	};

	componentDidMount(prevProps, prevState) {
		let dir = this;
		let ct = axios.CancelToken.source();
		axios.post(HOST_ADDR + '/api/church_directory/person/', {
			person_id: this.state.personId,
		},
		{
			cancelToken: ct.token,
		}).then((response) => {
			if (response.status === 200) {
				dir.setState({person: response.data});
				dir.cancelTokens.splice(dir.cancelTokens.indexOf(ct), 1);
			}
		}).catch((thrown) => {
		});
		this.cancelTokens.push(ct);
	}

	componentWillUnmount(prevProps, prevState) {
		for (let v of this.cancelTokens) {
			v.cancel();
		}
		this.cancelTokens = [];
	}

	emailBtn = (name, val) => {
		window.location.href = 'mailto:' + this.state.person.email_address;
	};

	cellPhoneBtn = (name, val) => {
		window.location.href = 'tel:+1' + this.state.person.cell_number;
	};

	homePhoneBtn = (name, val) => {
		window.location.href = 'tel:+1' + this.state.person.home_number;
	};

	render() {
		let p = this.state.person;
		let btnStyle = {margin: 5};
		return (
			<div style={{maxWidth: '900px', margin: '0 auto', display: 'flex'}}>
				<div style={{minWidth: '350px'}}>
					{
						p.image_url ? (
							<img
								src={'/api/' + p.image_url}
								alt={p.first_name + ' ' + p.last_name}
								width='97%'
							/>
						) : null
					}
				</div>
				<div style={{minWidth: '350px'}}>
					<Button raised='true' style={btnStyle} onClick={this.cellPhoneBtn} disabled={!p.cell_number}>
						Call Cell
					</Button>
					<Button raised='true' style={btnStyle} onClick={this.homePhoneBtn} disabled={!p.home_number}>
						Call Home
					</Button>
					<Button raised='true' style={btnStyle} onClick={this.emailBtn} disabled={!p.email_address}>
						Email
					</Button>
					<Button
						raised='true'
						style={btnStyle}
						color='secondary'
						component={Link}
						to={'/person/edit/' + this.state.personId + '/'}
					>
						Edit
					</Button>
					<Table>
						<TableBody>
							{this.buildRow('Name', p.first_name + ' ' + p.last_name)}
							{this.buildRow('Home Phone', p.home_number)}
							{this.buildRow('Cell Phone', p.cell_number)}
							{this.buildRow('Email', p.email_address)}
							{this.buildRow('City', p.city + ', ' + p.province)}
							{this.buildRow('Address', [p.address_line1, p.address_line2])}
							{this.buildRow('Birthday', p.birthday)}
						</TableBody>
					</Table>
				</div>
			</div>
		);
	}

};

export default PersonView;
