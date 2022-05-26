import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import './globals.dart';

Future<List<String>> fetchClasses(String raceid, String c) async {
  final response = await http.get(Uri.parse(
      '$apiUrlListClassification/default/results?id=$raceid&class=$c'));

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return List<String>.from(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load classification');
  }
}

class ClassificationRoute extends StatefulWidget {
  final String raceid;
  final String c;
  const ClassificationRoute(this.raceid, this.c, {Key? key}) : super(key: key);

  @override
  _ClassificationRouteState createState() => _ClassificationRouteState();
}

class _ClassificationRouteState extends State<ClassificationRoute> {
  late Future<List<String>> futureClasses;

  @override
  void initState() {
    super.initState();
    futureClasses = fetchClasses(widget.raceid, widget.c);
  }

  Future<void> _refreshData() async {
    futureClasses = fetchClasses(widget.raceid, widget.c);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Classification'),
      ),
      body: RefreshIndicator(
        onRefresh: _refreshData,
        child: FutureBuilder<List<String>>(
          future: futureClasses,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              List<String> classes = snapshot.data!;
              return ListView.builder(
                  itemCount: classes.length,
                  itemBuilder: ((context, index) => Text(
                        classes[index],
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
    );
  }
}
