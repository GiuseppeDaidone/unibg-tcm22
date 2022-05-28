import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import './globals.dart';
import './classification_route.dart';

Future<List<String>> fetchClasses(String raceid) async {
  final response = await http
      .get(Uri.parse('$apiUrlListClasses/default/list_classes?id=$raceid'));

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return List<String>.from(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception(
        'Nessuna categoria disponibile! La gara dovrà ancora svolgersi. Visualizza la griglia di partenza.');
  }
}

class ClassesRoute extends StatefulWidget {
  final String raceid;
  final String racename;
  const ClassesRoute(this.raceid, this.racename, {Key? key}) : super(key: key);

  @override
  _ClassesRouteState createState() => _ClassesRouteState();
}

class _ClassesRouteState extends State<ClassesRoute> {
  late Future<List<String>> futureClasses;

  @override
  void initState() {
    super.initState();
    futureClasses = fetchClasses(widget.raceid);
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
                "Categorie",
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
          future: futureClasses,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              List<String> classes = snapshot.data!;
              return ListView.builder(
                itemCount: classes.length,
                itemBuilder: ((context, index) => ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        primary: Colors.blue.shade700, // background
                      ),
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => ClassificationRoute(
                                widget.raceid, classes[index]),
                          ),
                        );
                      },
                      child: Text("\n" + classes[index] + "\n"),
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
