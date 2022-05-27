import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import './globals.dart';

Future<List<Map<String, dynamic>>> fetchAth(String raceid, String c) async {
  final response = await http.get(Uri.parse(
      '$apiUrlListAth/default/results_v2?id=$raceid&organisation=$c'));

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return List<Map<String, dynamic>>.from(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load classification');
  }
}

class AthRoute extends StatefulWidget {
  final String raceid;
  final String c;
  const AthRoute(this.raceid, this.c, {Key? key}) : super(key: key);

  @override
  _AthRouteState createState() => _AthRouteState();
}

class _AthRouteState extends State<AthRoute> {
  late Future<List<Map<String, dynamic>>> futureAth;

  @override
  void initState() {
    super.initState();
    futureAth = fetchAth(widget.raceid, widget.c);
  }

  Future<void> _refreshData() async {
    futureAth = fetchAth(widget.raceid, widget.c);
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
                "Atleti - Tempo",
                style: TextStyle(color: Colors.white, fontSize: 16.0),
              ),
              Text(
                widget.c,
                style: TextStyle(color: Colors.white, fontSize: 14.0),
              ),
            ]),
      ),
      body: Center(
        child: RefreshIndicator(
          onRefresh: _refreshData,
          child: FutureBuilder<List<Map<String, dynamic>>>(
            future: futureAth,
            builder: (context, snapshot) {
              if (snapshot.hasData) {
                var aths = snapshot.data!;
                return ListView.builder(
                    itemCount: aths.length,
                    itemBuilder: ((context, index) => Text(
                          aths[index]["Athlete"] +
                              " - " +
                              aths[index]["Time"] +
                              "s",
                          textAlign: TextAlign.center,
                          style: TextStyle(
                              fontSize: 18,
                              color: Colors.blue.shade900,
                              fontWeight: FontWeight.bold),
                        )));
              } else if (snapshot.hasError) {
                return Text('${snapshot.error}');
              }
              // By default, show a loading spinner.
              return const CircularProgressIndicator();
            },
          ),
        ),
      ),
    );
  }
}
