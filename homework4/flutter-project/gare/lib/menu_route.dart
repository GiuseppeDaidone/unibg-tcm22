import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import './globals.dart';
import './classes_route.dart';
import './club_route.dart';

class MenuRoute extends StatefulWidget {
  final String raceid;
  final String racename;
  const MenuRoute(this.raceid, this.racename, {Key? key}) : super(key: key);

  @override
  _MenuRouteState createState() => _MenuRouteState();
}

class _MenuRouteState extends State<MenuRoute> {
  @override
  void initState() {
    super.initState();
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
                "Filtra per",
                style: TextStyle(color: Colors.white, fontSize: 16.0),
              ),
              Text(
                widget.racename,
                style: TextStyle(color: Colors.white, fontSize: 14.0),
              ),
            ]),
      ),
      body: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(8),
        alignment: Alignment.topCenter,
        child: Column(
          children: [
            // An enabled button
            ElevatedButton(
              child: const Text('Categoria'),
              style: ElevatedButton.styleFrom(
                primary: Colors.blue.shade700, // background
              ),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) =>
                        ClassesRoute(widget.raceid, widget.racename),
                  ),
                );
              },
            ),
            const SizedBox(
              height: 8.0,
            ),
            // A disabled button
            ElevatedButton(
              child: const Text('Club'),
              style: ElevatedButton.styleFrom(
                primary: Colors.blue.shade700, // background
              ),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) =>
                        ClubRoute(widget.raceid, widget.racename),
                  ),
                );
              },
            )
          ],
        ),
      ),
    );
  }
}
