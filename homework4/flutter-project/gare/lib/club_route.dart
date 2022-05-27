import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import './globals.dart';
import './ath_route.dart';

Future<List<String>> fetchClubs(String raceid) async {
  final response =
      await http.get(Uri.parse('$apiUrlListClub/default/clubs?id=$raceid'));

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return List<String>.from(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load clubs');
  }
}

class ClubRoute extends StatefulWidget {
  final String raceid;
  final String racename;
  const ClubRoute(this.raceid, this.racename, {Key? key}) : super(key: key);

  @override
  _ClubRouteState createState() => _ClubRouteState();
}

class _ClubRouteState extends State<ClubRoute> {
  late Future<List<String>> futureClubs;

  @override
  void initState() {
    super.initState();
    futureClubs = fetchClubs(widget.raceid);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                "Club",
                style: TextStyle(color: Colors.white, fontSize: 16.0),
              ),
              Text(
                widget.racename,
                style: TextStyle(color: Colors.white, fontSize: 14.0),
              ),
            ]),
      ),
      body: Center(
        child: FutureBuilder<List<String>>(
          future: futureClubs,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              List<String> clubs = snapshot.data!;
              return ListView.builder(
                itemCount: clubs.length,
                itemBuilder: ((context, index) => ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        primary: Colors.blue.shade700, // background
                      ),
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) =>
                                AthRoute(widget.raceid, clubs[index]),
                          ),
                        );
                      },
                      child: Text(clubs[index]),
                    )),
              );
            } else if (snapshot.hasError) {
              return Text('${snapshot.error}');
            }
            // By default, show a loading spinner.
            return const CircularProgressIndicator();
          },
        ),
      ),
    );
  }
}
